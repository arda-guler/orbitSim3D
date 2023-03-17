from vector3 import *

def SymplecticEuler(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t, maneuver_auto_dt):
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

def VelocityVerlet(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, sim_time, delta_t, maneuver_auto_dt):
    
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
        if ad.vessels in vessels:
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
