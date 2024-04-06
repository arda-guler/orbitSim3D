import copy

from vector3 import *

def SymplecticEuler(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t):

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

    # GR
    for sch in schwarzschilds:
        accel = sch.compute_Schwarzschild()
        sch.vessel.update_vel(accel, delta_t)

    for lt in lensethirrings:
        accel = lt.compute_LenseThirring()
        lt.vessel.update_vel(accel, delta_t)

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
        x.update_traj_history()

    # update surface point positions
    for sp in surface_points:
        sp.update_state_vectors(delta_t)

def VelocityVerlet(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t):
    
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

    # calculate vessel accelerations due to relativistic effects
    for sch in schwarzschilds:
        if sch.vessel in vessels:
            v_idx = vessels.index(sch.vessel)
            accel_vec = sch.compute_Schwarzschild()
            vessel_accels_1[v_idx] = vessel_accels_1[v_idx] + accel_vec

    for lt in lensethirrings:
        if lt.vessel in vessels:
            v_idx = vessels.index(lt.vessel)
            accel_vec = lt.compute_LenseThirring()
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

    # calculate vessel accelerations due to relativistic effects
    for sch in schwarzschilds:
        if sch.vessel in vessels:
            v_idx = vessels.index(sch.vessel)
            accel_vec = sch.compute_Schwarzschild()
            vessel_accels_2[v_idx] = vessel_accels_2[v_idx] + accel_vec

    for lt in lensethirrings:
        if lt.vessel in vessels:
            v_idx = vessels.index(lt.vessel)
            accel_vec = lt.compute_LenseThirring()
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
        b.update_traj_history()

    for sp in surface_points:
        sp.update_state_vectors(delta_t)

    # update graphics related things
    for v in vessels:
        v.update_traj_history()
        v.update_draw_traj_history()

def Yoshida4(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t):

    # update masses and occultation calculations
    for ad in atmospheric_drags:
        ad.update_mass(maneuvers, sim_time, delta_t)

    for rp in radiation_pressures:
        rp.update_occultation(bodies)
        rp.update_mass(maneuvers, sim_time, delta_t)

    def compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t):
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

        # calculate vessel accelerations due to relativistic effects
        for sch in schwarzschilds:
            if sch.vessel in vessels:
                v_idx = vessels.index(sch.vessel)
                accel_vec = sch.compute_Schwarzschild()
                vessel_accels[v_idx] = vessel_accels[v_idx] + accel_vec

        for lt in lensethirrings:
            if lt.vessel in vessels:
                v_idx = vessels.index(lt.vessel)
                accel_vec = lt.compute_LenseThirring()
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
    vacc, bacc = compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t)
    update_objs_vel(vessels, bodies, d1, vacc, bacc, delta_t)

    update_objs_pos(vessels, bodies, c2, delta_t)
    vacc, bacc = compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t)
    update_objs_vel(vessels, bodies, d2, vacc, bacc, delta_t)

    update_objs_pos(vessels, bodies, c3, delta_t)
    vacc, bacc = compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t)
    update_objs_vel(vessels, bodies, d3, vacc, bacc, delta_t)

    update_objs_pos(vessels, bodies, c4, delta_t)

    # this has to be done separately
    for m in maneuvers:
        m.update_mass(sim_time, delta_t)

    # planet orientation update
    for b in bodies:
        b.update_orient(delta_t)
        b.update_traj_history()

    for sp in surface_points:
        sp.update_state_vectors(delta_t)

    # update graphics related things
    for v in vessels:
        v.update_traj_history()
        v.update_draw_traj_history()

def Yoshida8(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t):
    # update masses and occultation calculations
    for ad in atmospheric_drags:
        ad.update_mass(maneuvers, sim_time, delta_t)

    for rp in radiation_pressures:
        rp.update_occultation(bodies)
        rp.update_mass(maneuvers, sim_time, delta_t)

    def compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t):
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

        # calculate vessel accelerations due to relativistic effects
        for sch in schwarzschilds:
            if sch.vessel in vessels:
                v_idx = vessels.index(sch.vessel)
                accel_vec = sch.compute_Schwarzschild()
                vessel_accels[v_idx] = vessel_accels[v_idx] + accel_vec

        for lt in lensethirrings:
            if lt.vessel in vessels:
                v_idx = vessels.index(lt.vessel)
                accel_vec = lt.compute_LenseThirring()
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
    w1 = 0.311790812418427e0
    w2 = -0.155946803821447e1
    w3 = -0.167896928259640e1
    w4 = 0.166335809963315e1
    w5 = -0.106458714789183e1
    w6 = 0.136934946416871e1
    w7 = 0.629030650210433e0
    w0 = 1.65899088454396 # (1 - 2 * (w1 + w2 + w3 + w4 + w5 + w6 + w7))

    ds = [w7, w6, w5, w4, w3, w2, w1, w0, w1, w2, w3, w4, w5, w6, w7]

    # cs = [w7 / 2, (w7 + w6) / 2, (w6 + w5) / 2, (w5 + w4) / 2,
    #           (w4 + w3) / 2, (w3 + w2) / 2, (w2 + w1) / 2, (w1 + w0) / 2,
    #           (w1 + w0) / 2, (w2 + w1) / 2, (w3 + w2) / 2, (w4 + w3) / 2,
    #           (w5 + w4) / 2, (w6 + w5) / 2, (w7 + w6) / 2, w7 / 2]

    cs = [0.3145153251052165, 0.9991900571895715, 0.15238115813844, 0.29938547587066, -0.007805591481624963,
          -1.619218660405435, -0.6238386128980216, 0.9853908484811935, 0.9853908484811935, -0.6238386128980216,
          -1.619218660405435, -0.007805591481624963, 0.29938547587066, 0.15238115813844, 0.9991900571895715,
          0.3145153251052165]

    for i in range(15):
        update_objs_pos(vessels, bodies, cs[i], delta_t)
        vacc, bacc = compute_accels_at_state(vessels, bodies, maneuvers, atmospheric_drags, radiation_pressures,
                                             schwarzschilds, lensethirrings, sim_time, delta_t)
        update_objs_vel(vessels, bodies, ds[i], vacc, bacc, delta_t)

    update_objs_pos(vessels, bodies, cs[15], delta_t)

    # this has to be done separately
    for m in maneuvers:
        m.update_mass(sim_time, delta_t)

    # planet orientation update
    for b in bodies:
        b.update_orient(delta_t)
        b.update_traj_history()

    for sp in surface_points:
        sp.update_state_vectors(delta_t)

    # update graphics related things
    for v in vessels:
        v.update_traj_history()
        v.update_draw_traj_history()

def adaptive(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t,
             solver_type=0, tolerance=1e-8):

    c_delta_t = delta_t
    z_delta_t = delta_t * 0.5

    def copylist(inlist):
        outlist = []
        for obj in inlist:
            outlist.append(copy.copy(obj))

        return outlist

    good_step = False
    increase_delta_t = False
    while not good_step:
        # safekeep original states, use copies for computations
        c_bodies = copylist(bodies)
        c_vessels = copylist(vessels)
        c_surface_points = copylist(surface_points)
        c_maneuvers = copylist(maneuvers)
        c_atmospheric_drags = copylist(atmospheric_drags)
        c_radiation_pressures = copylist(radiation_pressures)
        c_schwarzschilds = copylist(schwarzschilds)
        c_lensethirrings = copylist(lensethirrings)
        c_sim_time = sim_time

        # solve the step using delta_t
        if solver_type == 0:
            SymplecticEuler(c_bodies, c_vessels, c_surface_points, c_maneuvers, c_atmospheric_drags, c_radiation_pressures, c_schwarzschilds, c_lensethirrings, c_sim_time, c_delta_t)
        elif solver_type == 1:
            VelocityVerlet(c_bodies, c_vessels, c_surface_points, c_maneuvers, c_atmospheric_drags, c_radiation_pressures, c_schwarzschilds, c_lensethirrings, c_sim_time, c_delta_t)
        elif solver_type == 2:
            Yoshida4(c_bodies, c_vessels, c_surface_points, c_maneuvers, c_atmospheric_drags, c_radiation_pressures, c_schwarzschilds, c_lensethirrings, c_sim_time, c_delta_t)
        else:
            Yoshida8(c_bodies, c_vessels, c_surface_points, c_maneuvers, c_atmospheric_drags, c_radiation_pressures, c_schwarzschilds, c_lensethirrings, c_sim_time, c_delta_t)

        # save results
        d1_positions = []
        for obj in c_bodies:
            d1_positions.append(obj.pos)

        for obj in c_vessels:
            d1_positions.append(obj.pos)

        # solve the step using using delta_t / 2
        z_bodies = copylist(bodies)
        z_vessels = copylist(vessels)
        z_surface_points = copylist(surface_points)
        z_maneuvers = copylist(maneuvers)
        z_atmospheric_drags = copylist(atmospheric_drags)
        z_radiation_pressures = copylist(radiation_pressures)
        z_schwarzschilds = copylist(schwarzschilds)
        z_lensethirrings = copylist(lensethirrings)
        z_sim_time = sim_time

        if solver_type == 0:
            SymplecticEuler(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)
            SymplecticEuler(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)
        elif solver_type == 1:
            VelocityVerlet(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)
            VelocityVerlet(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)
        elif solver_type == 2:
            Yoshida4(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)
            Yoshida4(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)
        else:
            Yoshida8(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)
            Yoshida8(z_bodies, z_vessels, z_surface_points, z_maneuvers, z_atmospheric_drags, z_radiation_pressures, z_schwarzschilds, z_lensethirrings, z_sim_time, z_delta_t)

        # save results
        d2_positions = []
        for obj in z_bodies:
            d2_positions.append(obj.pos)

        for obj in z_vessels:
            d2_positions.append(obj.pos)

        # compare all
        if len(d1_positions) == len(d2_positions):
            errors = []
            for i in range(len(d1_positions)):
                errors.append((d1_positions[i] - d2_positions[i]).mag())

            for e in errors:
                if e > tolerance:
                    delta_t = 0.5 * delta_t
                else:
                    good_step = True
                    if e < tolerance * 0.3:
                        increase_delta_t = True

        else:
            pass # something changed during this step - can't compare

    if solver_type == 0:
        SymplecticEuler(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t)
    elif solver_type == 1:
        VelocityVerlet(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t)
    elif solver_type == 2:
        Yoshida4(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t)
    elif solver_type == 3:
        Yoshida8(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, schwarzschilds, lensethirrings, sim_time, delta_t)
    
    return delta_t, increase_delta_t
    
# def RK89() ?
# Maybe with a not-energy-conserving warning.
