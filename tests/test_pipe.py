#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pytest import approx, raises
from jeppson.pipe import Pipe, SimplePipe, SimpleCHWPipe, SimpleEFPipe, \
                         ureg, Q_
import scipy.constants as sc

__author__ = "Bob Apthorpe"
__copyright__ = "Bob Apthorpe"
__license__ = "mit"


def test_simple_pipe():
    p1 = SimplePipe(label='Pipe 1', length=100.0 * ureg.foot,
                    idiameter=12.0 * ureg.inch)
    assert p1.label == 'Pipe 1'
    assert p1.length.to('m').magnitude == approx(30.48)
    assert p1.idiameter.to('m').magnitude == approx(0.3048)
    assert p1.ld_ratio.to_base_units().magnitude == approx(100.0)
    assert p1.flow_area.to('m**2').magnitude == approx(0.07296587699003966)

    with raises(ValueError):
        p1.ld_ratio = Q_(50.0, '')

    with raises(ValueError):
        p1.flow_area = Q_(2.9186E-1, 'm**2')

    with raises(ValueError):
        p1.length = Q_(1200.0, 'm')

    with raises(ValueError):
        p1.length = Q_(9.0E-4, 'm')

    with raises(ValueError):
        p1.idiameter = Q_(35.0, 'ft')

    with raises(ValueError):
        p1.idiameter = Q_(9.0E-4, 'm')

    p2 = SimplePipe(label='Pipe 2', length=100.0 * ureg.foot,
                    idiameter=12.0 * ureg.inch)

    p2.length = Q_(50.0, 'ft')
    assert p2.length.to('m').magnitude == approx(15.24)
    assert p2.idiameter.to('m').magnitude == approx(0.3048)
    assert p2.ld_ratio.to_base_units().magnitude == approx(50.0)
    assert p2.flow_area.to('m**2').magnitude == approx(0.07296587699003966)

    p2.idiameter = Q_(24.0, 'in')
    assert p2.length.to('m').magnitude == approx(15.24)
    assert p2.idiameter.to('m').magnitude == approx(0.6096)
    assert p2.ld_ratio.to_base_units().magnitude == approx(25.0)
    assert p2.flow_area.to('m**2').magnitude == approx(0.291863261)

    return

def test_simple_chw_pipe():
    p1 = SimpleCHWPipe(label='Pipe 1', length=100.0 * ureg.foot,
                    idiameter=12.0 * ureg.inch, chw=150.0)
    assert p1.label == 'Pipe 1'
    assert p1.length.to('m').magnitude == approx(30.48)
    assert p1.idiameter.to('m').magnitude == approx(0.3048)
    assert p1.ld_ratio.to_base_units().magnitude == approx(100.0)
    assert p1.flow_area.to('m**2').magnitude == approx(0.07296587699003966)
    assert p1.chw == approx(150.0)

    p1.chw = 130.0
    assert p1.chw == approx(130.0)

    with raises(ValueError):
        p1.chw = -4.0

    with raises(ValueError):
        p1.chw = 3600.0

def test_simple_ef_pipe():
    p1 = SimpleEFPipe(label='Pipe 1', length=100.0 * ureg.foot,
                    idiameter=12.0 * ureg.inch, eroughness=8.5E-4)
    assert p1.label == 'Pipe 1'
    assert p1.length.to('m').magnitude == approx(30.48)
    assert p1.idiameter.to('m').magnitude == approx(0.3048)
    assert p1.ld_ratio.to_base_units().magnitude == approx(100.0)
    assert p1.flow_area.to('m**2').magnitude == approx(0.07296587699003966)
    assert p1.eroughness == approx(8.5E-4)
    assert p1.froughness.to('in').magnitude == approx(1.02E-2)

    p1.froughness = 2.04E-2 * ureg.inch
    assert p1.eroughness == approx(1.7E-3)

    with raises(ValueError):
        p1.eroughness = -0.0004

    with raises(ValueError):
        p1.eroughness = 0.1001

    with raises(ValueError):
        p1.froughness = -0.0004 * ureg.inch

    with raises(ValueError):
        p1.froughness = 0.1001 * p1.idiameter

    with raises(ValueError):
        p1.vol_flow = Q_(0.5, 'ft**3/s')

    with raises(ValueError):
        print(p1.vol_flow)

    with raises(ValueError):
        p1.kin_visc = Q_(1.217E-5, 'ft**2/s')

    with raises(ValueError):
        print(p1.kin_visc)

    with raises(ValueError):
        p1.vflow = Q_(5.0, 'ft/s')

    with raises(ValueError):
        print(p1.vflow)

    with raises(ValueError):
        p1.Re = 500000.0

    with raises(ValueError):
        print(p1.Re)

    with raises(ValueError):
        p1.friction = 0.0014

    with raises(ValueError):
        print(p1.friction)

    p1 = SimpleEFPipe(label='Pipe 1', length=150.0 * ureg.foot,
                    idiameter=4.0 * ureg.inch, froughness=7.0E-6 * ureg.foot)

    p1.set_flow_conditions(vol_flow=Q_(0.5, 'ft**3/s'),
                           kin_visc=Q_(1.217E-5, 'ft**2/s'))

    assert p1.vol_flow.to('ft**3/s').magnitude == approx(0.5)
    assert p1.kin_visc.to('ft**2/s').magnitude == approx(1.217E-5)
    assert p1.vflow.to('ft/s').magnitude == approx(5.72957795)
    assert p1.Re == approx(156931.7)
    assert p1.friction == approx(0.016554318)

def test_pipe():
    p1 = Pipe(label='Pipe 1', length=100.0 * sc.foot, 
              idiameter=12.0 * sc.inch, odiameter=12.5 * sc.inch,
              eroughness=8.5E-4)
    assert p1.label == 'Pipe 1'
    assert p1.length == approx(30.48)
    assert p1.idiameter == approx(0.3048)
    assert p1.eroughness == approx(8.5E-4)

    assert p1.as_table(headers=['length', 'idiameter', 'eroughness'])

    p2 = Pipe(label='Pipe 2', length=100.0 * sc.foot, 
              idiameter=12.0 * sc.inch, twall=0.25 * sc.inch,
              eroughness=8.5E-4)

    assert p2.odiameter == approx(12.5 * sc.inch)
    assert p2.twall == approx(0.25 * sc.inch)
    assert p2.idiameter == approx(12.0 * sc.inch)
    assert p2.flow_area == approx(7.2965877E-2)

    p2.odiameter = 13.0 * sc.inch
    assert p2.idiameter == approx(12.0 * sc.inch)
    assert p2.odiameter == approx(13.0 * sc.inch)
    assert p2.twall == approx(0.5 * sc.inch)

    p2.twall = 0.25 * sc.inch
    assert p2.idiameter == approx(12.0 * sc.inch)
    assert p2.odiameter == approx(12.5 * sc.inch)
    assert p2.twall == approx(0.25 * sc.inch)

    p2.idiameter = 12.25 * sc.inch
    assert p2.idiameter == approx(12.25 * sc.inch)
    assert p2.odiameter == approx(12.5 * sc.inch)
    assert p2.twall == approx(0.125 * sc.inch)

    with raises(ValueError):
        p2.idiameter = 1.0E-4

    with raises(ValueError):
        p2.idiameter = 11.0

    with raises(ValueError):
        p2.odiameter = 1.0E-4

    with raises(ValueError):
        p2.odiameter = 11.0

    with raises(ValueError):
        p2.twall = 1.0E-6

    with raises(ValueError):
        p2.twall = 1.01

    with raises(ValueError):
        p2.eroughness = -1.0E-6

    with raises(ValueError):
        p2.eroughness = 0.2

    with raises(ValueError):
        p2.length = 1.0E-4

    with raises(ValueError):
        p2.length = 1001.0

    with raises(ValueError):
        p2.flow_area = 7.2965877E-2
        
    with raises(ValueError):
        p2.nearest_material_roughness('cheese', is_clean=False)

    p2.nearest_material_roughness('cast iron', is_clean=True)
    assert p2.eroughness == approx(2.59E-4)

    p2.nearest_dimensions_from_schedule('80')
    # The schedule 80 pipe size with an inner diameter closest to 12" is
    # 14" with Di = 12.75", Do = 14.0, and twall = 0.75"
    assert p2._twall == approx(0.75 * sc.inch)
    assert p2._odiameter == approx(14.0 * sc.inch)
    assert p2.idiameter == approx(12.5 * sc.inch)

    with raises(ValueError):
        p2.nearest_dimensions_from_schedule(schedule='80', dnominal=120)

    p2.nearest_dimensions_from_schedule(schedule='80', dnominal=12)
    assert p2.idiameter == approx(11.38 * sc.inch, abs=1.0E-3)
    assert p2._odiameter == approx(12.75 * sc.inch, abs=1.0E-3)
    assert p2._twall == approx((p2._odiameter - p2.idiameter) / 2.0)

    p2.odiameter = 38.0 * sc.inch
    p2.idiameter = 36.0 * sc.inch
    with raises(ValueError):
        p2.nearest_dimensions_from_schedule(schedule='80')

    with raises(ValueError):
        p2.clean = 'manky'

    with raises(ValueError):
        p2.surface = 'smooth'

    # 12" Schedule 80 pipe has a Di of 11.38", Do = 12.75", and twall = 0.68"
    p3 = Pipe(label='Pipe 3', length=10.0 * sc.foot, 
              idiameter=11.37 * sc.inch, schedule='80',
              eroughness=8.5E-4)

    assert p3.idiameter == approx(11.38 * sc.inch, abs=1.0E-3)
    assert p3._odiameter == approx(12.75 * sc.inch, abs=1.0E-3)
    assert p3._twall == approx((p3._odiameter - p3.idiameter) / 2.0)

    # 12" Schedule 80 pipe has a Di of 11.38", Do = 12.75", and twall = 0.68"
    p4 = Pipe(label='Pipe 4', length=10.0 * sc.foot, 
              idiameter=11.37 * sc.inch, 
              odiameter=12.75 * sc.inch, 
              eroughness=8.5E-4)

    assert p4._twall == approx((p4._odiameter - p4.idiameter) / 2.0)

    # 12" Schedule 80 pipe has a Di of 11.38", Do = 12.75", and twall = 0.68"
    p5 = Pipe(label='Pipe 5', length=10.0 * sc.foot, 
              idiameter=11.37 * sc.inch, 
              twall=0.68 * sc.inch, 
              eroughness=8.5E-4)

    assert p5._odiameter == approx(12.75 * sc.inch, abs=1.0E-3)

    # 12" Schedule 80 pipe has a Di of 11.38", Do = 12.75", and twall = 0.68"
    p6 = Pipe(label='Pipe 6', length=10.0 * sc.foot, 
              schedule='80', nps=12)

    assert p6.idiameter == approx(11.38 * sc.inch, abs=1.0E-3)
    assert p6._odiameter == approx(12.75 * sc.inch, abs=1.0E-3)
    assert p6._twall == approx((p6._odiameter - p6.idiameter) / 2.0)
    assert p6.eroughness == 0.0
    assert p6.as_table(headers=['length', 'idiameter', 'eroughness'])

    # 12" Schedule 80 pipe has a Di of 11.38", Do = 12.75", and twall = 0.68"
    p7 = Pipe(label='Pipe 7', length=10.0 * sc.foot, 
              schedule='80', nps=12, froughness=2.46850408E-4)

    assert p7.idiameter == approx(11.38 * sc.inch, abs=1.0E-3)
    assert p7._odiameter == approx(12.75 * sc.inch, abs=1.0E-3)
    assert p7._twall == approx((p7._odiameter - p7.idiameter) / 2.0)
    assert p7.flow_area == approx(6.5524E-2, abs=1.0E-6)
    assert p7.eroughness == approx(8.54E-4, abs=1.0E-6)

    p7 = Pipe(label='Pipe 7', length=10.0 * sc.foot, 
              schedule='80', nps=12, surface='cast iron')

    assert p7.eroughness == approx(2.59E-4)

    p7 = Pipe(label='Pipe 7', length=10.0 * sc.foot, 
              schedule='80', nps=12, surface='Steel tubes', is_clean=False)

    assert p7.eroughness == approx(1.0E-3)

    p8 = Pipe(label='Pipe 8', length=30.0 * sc.foot)
    p8.twall = 0.5 * sc.inch
    p8.idiameter = 12 * sc.inch
    assert p8.idiameter == approx(12 * sc.inch)
    assert p8.odiameter == approx(13 * sc.inch)
    assert p8.twall == approx(0.5 * sc.inch)

    p8 = Pipe(label='Pipe 8', length=30.0 * sc.foot)
    p8.twall = 0.5 * sc.inch
    p8.odiameter = 13 * sc.inch
    assert p8.idiameter == approx(12 * sc.inch)
    assert p8.odiameter == approx(13 * sc.inch)
    assert p8.twall == approx(0.5 * sc.inch)

    return
