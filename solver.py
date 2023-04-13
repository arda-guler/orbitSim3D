from vector3 import *

def SymplecticEuler(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t):
    # update physics
    for rp in radiation_pressures:
        rp.update_occultation(bodies)
        rp.update_mass(maneuvers, sim_time, delta_t)
        accel = rp.calc_accel()
        rp.vessel.update_vel(accel, delta_t)
        # do not update vessel position in this 'for' loop, we did not apply all accelerations!

    for ad in atmospheric_drags:
        ad.update_mass(maneuvers, sim_time, delta_t)
        accel = ad.calc_accel()
        ad.vessel.update_vel(accel, delta_t)
        # do not update vessel position in this 'for' loop, we did not apply all accelerations!

    for m in maneuvers:
        m.perform_maneuver(sim_time, delta_t)

    for v in vessels:
        accel = vec3(0, 0, 0)

        for b in bodies:
            accel = accel + v.get_gravity_by(b)

        v.update_vel(accel, delta_t)

    for x in bodies:
        accel = vec3(0, 0, 0)
        for y in bodies:
            if not x == y:  # don't attempt to apply gravity to self
                accel = accel + x.get_gravity_by(y)

        x.update_vel(accel, delta_t)

    # update positions after all accelerations are calculated
    for v in vessels:
        v.update_pos(delta_t)
        v.update_traj_history()
        v.update_draw_traj_history()

    for x in bodies:
        x.update_pos(delta_t)

        # planets rotate!
        x.update_orient(delta_t)

    # update surface point positions
    for sp in surface_points:
        sp.update_state_vectors(delta_t)

def VelocityVerlet(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t):
    
    # update masses and occultation calculations
    for ad in atmospheric_drags:
        ad.update_mass(maneuvers, sim_time, delta_t)

    for rp in radiation_pressures:
        rp.update_occultation(bodies)
        rp.update_mass(maneuvers, sim_time, delta_t)
        
    # - - - FIRST ACCELERATIONS - - -
    vessel_accels_1 = [vec3(0, 0, 0)] * len(vessels)
    body_accels_1 = [vec3(0, 0, 0)] * len(bodies)

    # calculate celestial body accelerations due to gravity
    for x in bodies:
        for y in bodies:
            if not x == y:
                b_idx = bodies.index(x)
                body_accels_1[b_idx] = body_accels_1[b_idx] + x.get_gravity_by(y)

    # calculate vessel accelerations due to gravity
    for v in vessels:
        v_idx = vessels.index(v)
        for b in bodies:
            vessel_accels_1[v_idx] = vessel_accels_1[v_idx] + v.get_gravity_by(b)

    # calculate vessel accelerations due to maneuvers
    for m in maneuvers:
        if m.vessel in vessels:
            v_idx = vessels.index(m.vessel)
            accel_vec = m.get_accel(sim_time, delta_t)
            vessel_accels_1[v_idx] = vessel_accels_1[v_idx] + accel_vec

    # calculate vessel accelerations due to atmospheric drag
    for ad in atmospheric_drags:
        if ad.vessel in vessels:
            v_idx = vessels.index(ad.vessel)
            accel_vec = ad.calc_accel()
            vessel_accels_1[v_idx] = vessel_accels_1[v_idx] + accel_vec

    # calculate vessel accelerations due to radiation pressure
    for rp in radiation_pressures:
        if rp.vessel in vessels:
            v_idx = vessels.index(rp.vessel)
            accel_vec = rp.calc_accel()
            vessel_accels_1[v_idx] = vessel_accels_1[v_idx] + accel_vec

    # - - - POSITION UPDATE - - -
    for b in bodies:
        b_idx = bodies.index(b)
        b.set_pos(b.pos + b.vel * delta_t + body_accels_1[b_idx] * 0.5 * delta_t**2)

    for v in vessels:
        v_idx = vessels.index(v)
        v.set_pos(v.pos + v.vel * delta_t + vessel_accels_1[v_idx] * 0.5 * delta_t**2)

    # - - - SECOND ACCELERATIONS - - -
    vessel_accels_2 = [vec3(0, 0, 0)] * len(vessels)
    body_accels_2 = [vec3(0, 0, 0)] * len(bodies)

    # calculate celestial body accelerations due to gravity
    for x in bodies:
        for y in bodies:
            if not x == y:
                b_idx = bodies.index(x)
                body_accels_2[b_idx] = body_accels_2[b_idx] + x.get_gravity_by(y)

    # calculate vessel accelerations due to gravity
    for v in vessels:
        v_idx = vessels.index(v)
        for b in bodies:
            vessel_accels_2[v_idx] = vessel_accels_2[v_idx] + v.get_gravity_by(b)

    # calculate vessel accelerations due to maneuvers
    for m in maneuvers:
        if m.vessel in vessels:
            v_idx = vessels.index(m.vessel)
            accel_vec = m.get_accel((sim_time + delta_t), delta_t)
            vessel_accels_2[v_idx] = vessel_accels_2[v_idx] + accel_vec

    # calculate vessel accelerations due to atmospheric drag
    for ad in atmospheric_drags:
        if ad.vessel in vessels:
            v_idx = vessels.index(ad.vessel)
            accel_vec = ad.calc_accel()
            vessel_accels_2[v_idx] = vessel_accels_2[v_idx] + accel_vec

    # calculate vessel accelerations due to radiation pressure
    for rp in radiation_pressures:
        if rp.vessel in vessels:
            v_idx = vessels.index(rp.vessel)
            accel_vec = rp.calc_accel()
            vessel_accels_2[v_idx] = vessel_accels_2[v_idx] + accel_vec

    # - - - VELOCITY UPDATE - - -
    for b in bodies:
        b_idx = bodies.index(b)
        b.set_vel(b.vel + (body_accels_1[b_idx] + body_accels_2[b_idx]) * 0.5 * delta_t)

    for v in vessels:
        v_idx = vessels.index(v)
        v.set_vel(v.vel + (vessel_accels_1[v_idx] + vessel_accels_2[v_idx]) * 0.5 * delta_t)

    for m in maneuvers:
        m.update_mass(sim_time, delta_t)

    # planet orientation update
    for b in bodies:
        b.update_orient(delta_t)

    for sp in surface_points:
        sp.update_state_vectors(delta_t)

    # update graphics related things
    for v in vessels:
        v.update_traj_history()
        v.update_draw_traj_history()

def Yoshida4(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t):

    # update masses and occultation calculations
    for ad in atmospheric_drags:
        ad.update_mass(maneuvers, sim_time, delta_t)

    for rp in radiation_pressures:
        rp.update_occultation(bodies)
        rp.update_mass(maneuvers, sim_time, delta_t)

    def compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t):
        vessel_accels = [vec3(0, 0, 0)] * len(vessels)
        body_accels = [vec3(0, 0, 0)] * len(bodies)

        # calculate celestial body accelerations due to gravity
        for x in bodies:
            for y in bodies:
                if not x == y:
                    b_idx = bodies.index(x)
                    body_accels[b_idx] = body_accels[b_idx] + x.get_gravity_by(y)

        # calculate vessel accelerations due to gravity
        for v in vessels:
            v_idx = vessels.index(v)
            for b in bodies:
                vessel_accels[v_idx] = vessel_accels[v_idx] + v.get_gravity_by(b)

        # calculate vessel accelerations due to maneuvers
        for m in maneuvers:
            if m.vessel in vessels:
                v_idx = vessels.index(m.vessel)
                accel_vec = m.get_accel(sim_time, delta_t)
                vessel_accels[v_idx] = vessel_accels[v_idx] + accel_vec

        # calculate vessel accelerations due to atmospheric drag
        for ad in atmospheric_drags:
            if ad.vessel in vessels:
                v_idx = vessels.index(ad.vessel)
                accel_vec = ad.calc_accel()
                vessel_accels[v_idx] = vessel_accels[v_idx] + accel_vec

        # calculate vessel accelerations due to radiation pressure
        for rp in radiation_pressures:
            if rp.vessel in vessels:
                v_idx = vessels.index(rp.vessel)
                accel_vec = rp.calc_accel()
                vessel_accels[v_idx] = vessel_accels[v_idx] + accel_vec

        return vessel_accels, body_accels

    def update_objs_pos(vessels, bodies, const, dt):
        for v in vessels:
            v.pos = v.pos + v.vel * const * dt

        for b in bodies:
            b.pos = b.pos + b.vel * const * dt

    def update_objs_vel(vessels, bodies, const, vacc, bacc, dt):
        for idx_v, v in enumerate(vessels):
            v.vel = v.vel + vacc[idx_v] * const * dt

        for idx_b, b in enumerate(bodies):
            b.vel = b.vel + bacc[idx_b] * const * dt

    # - - - CONSTANTS - - -
    # w0 = -1.7024143839193153
    # w1 = 1.3512071919596578
    c1 = 0.6756035959798289
    c2 = -0.17560359597982877
    c3 = -0.17560359597982877
    c4 = 0.6756035959798289
    d1 = 1.3512071919596578
    d2 = -1.7024143839193153
    d3 = 1.3512071919596578

    update_objs_pos(vessels, bodies, c1, delta_t)
    vacc, bacc = compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t)
    update_objs_vel(vessels, bodies, d1, vacc, bacc, delta_t)

    update_objs_pos(vessels, bodies, c2, delta_t)
    vacc, bacc = compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t)
    update_objs_vel(vessels, bodies, d2, vacc, bacc, delta_t)

    update_objs_pos(vessels, bodies, c3, delta_t)
    vacc, bacc = compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t)
    update_objs_vel(vessels, bodies, d3, vacc, bacc, delta_t)

    update_objs_pos(vessels, bodies, c4, delta_t)

    # this has to be done separately
    for m in maneuvers:
        m.update_mass(sim_time, delta_t)

    # planet orientation update
    for b in bodies:
        b.update_orient(delta_t)

    for sp in surface_points:
        sp.update_state_vectors(delta_t)

    # update graphics related things
    for v in vessels:
        v.update_traj_history()
        v.update_draw_traj_history()

# def RK89() ?
# Maybe with a not-energy-conserving warning.
