#!/usr/bin/env python3
import unittest
import socket

from hs110exporter import validIP, HS110data

class TestValidIP(unittest.TestCase):
  def test_ipstring(self):
    self.assertEqual(validIP('192.168.0.1'), '192.168.0.1')
    self.assertEqual(validIP(' 192.168.0.1 '), '192.168.0.1')

  def test_ipvalues(self):
    self.assertRaises(TypeError, validIP, 192)
    self.assertRaises(TypeError, validIP, 192.168)
    self.assertRaises(TypeError, validIP, 3j)
    self.assertRaises(ValueError, validIP, '192.168.0.1.a')

class TestHS110data(unittest.TestCase):
  def test_encryptstring(self):
    hs110 = HS110data()
    text_encrypted = b'\x00\x00\x00\x10\xd0\xf0\x98\xfd\x91\xfd\x92\xa8\x88\xff\x90\xe2\x8e\xea\xca\xb7'
    text_decrypted = '{ hello: world }'

    self.assertEqual(hs110._HS110data__encrypt(text_decrypted), text_encrypted)
    self.assertEqual(hs110._HS110data__decrypt(text_encrypted), text_decrypted)


  def test_encryptvalues(self):
    hs110 = HS110data()

    self.assertRaises(TypeError, hs110._HS110data__encrypt, 100)
    self.assertRaises(TypeError, hs110._HS110data__encrypt, 100.1)
    self.assertRaises(TypeError, hs110._HS110data__encrypt, 3j)
    self.assertRaises(TypeError, hs110._HS110data__encrypt, b'\x00\x00\x00\x10')
    self.assertIsInstance(hs110._HS110data__encrypt('Hello world'), bytes)

  def test_decryptvalues(self):
    hs110 = HS110data()

    self.assertRaises(TypeError, hs110._HS110data__decrypt, 100)
    self.assertRaises(TypeError, hs110._HS110data__decrypt, 100.1)
    self.assertRaises(TypeError, hs110._HS110data__decrypt, 3j)
    self.assertRaises(TypeError, hs110._HS110data__decrypt, "Hello world")
    self.assertIsInstance(hs110._HS110data__decrypt(b'\x00\x00\x00\x10'), str)

  def test_received_data(self):

    for h in ['h1', 'h2']:
      hs110 = HS110data(h)
      self.assertRaises(TypeError, hs110.get_data, 100)
      self.assertRaises(TypeError, hs110.get_data, 100.1)
      self.assertRaises(TypeError, hs110.get_data, 3j)
      self.assertRaises(ValueError, hs110.get_data, "nonexist")

      self.assertEqual(hs110.get_data('power'), 0)
      self.assertEqual(hs110.get_data('current'), 0)
      self.assertEqual(hs110.get_data('voltage'), 0)
      self.assertEqual(hs110.get_data('total'), 0)


  def test_receive(self):
    # current=0.342122, voltage=239.527888, power=66.941523, total=10.155, err_code=0
    sample_data_ok = b'\x00\x00\x00v\xd0\xf2\x97\xfa\x9f\xeb\x8e\xfc\xde\xe4\x9f\xbd\xda\xbf\xcb\x94\xe6\x83\xe2\x8e\xfa\x93\xfe\x9b\xb9\x83\xf8\xda\xb9\xcc\xbe\xcc\xa9\xc7\xb3\x91\xab\x9b\xb5\x86\xb2\x80\xb1\x83\xb1\x9d\xbf\xc9\xa6\xca\xbe\xdf\xb8\xdd\xff\xc5\xf7\xc4\xfd\xd3\xe6\xd4\xe3\xdb\xe3\xdb\xf7\xd5\xa5\xca\xbd\xd8\xaa\x88\xb2\x84\xb2\x9c\xa5\x91\xa0\x95\xa7\x94\xb8\x9a\xee\x81\xf5\x94\xf8\xda\xe0\xd1\xe1\xcf\xfe\xcb\xfe\xce\xfe\xce\xe2\xc0\xa5\xd7\xa5\xfa\x99\xf6\x92\xf7\xd5\xef\xdf\xa2\xdf\xa2'
    sample_data_fail = b'\x00\x00\x00v\xd0\xf2\x97\xfa'

    #  '{"emeter":{"get_realtime":{"current_ma":0.342122,"voltage_mv":239.527888,"power_mw":66.941523,"total_wh":10.155000,"err_code":0}}}'
    sample_data_h2 = b'\x00\x00\x00\x82\xd0\xf2\x97\xfa\x9f\xeb\x8e\xfc\xde\xe4\x9f\xbd\xda\xbf\xcb\x94\xe6\x83\xe2\x8e\xfa\x93\xfe\x9b\xb9\x83\xf8\xda\xb9\xcc\xbe\xcc\xa9\xc7\xb3\xec\x81\xe0\xc2\xf8\xc8\xe6\xd5\xe1\xd3\xe2\xd0\xe2\xce\xec\x9a\xf5\x99\xed\x8c\xeb\x8e\xd1\xbc\xca\xe8\xd2\xe0\xd3\xea\xc4\xf1\xc3\xf4\xcc\xf4\xcc\xe0\xc2\xb2\xdd\xaa\xcf\xbd\xe2\x8f\xf8\xda\xe0\xd6\xe0\xce\xf7\xc3\xf2\xc7\xf5\xc6\xea\xc8\xbc\xd3\xa7\xc6\xaa\xf5\x82\xea\xc8\xf2\xc3\xf3\xdd\xec\xd9\xec\xdc\xec\xdc\xf0\xd2\xb7\xc5\xb7\xe8\x8b\xe4\x80\xe5\xc7\xfd\xcd\xb0\xcd\xb0'
    hs110 = HS110data()

    self.assertRaises(ValueError, hs110.receive, 'this is a string')
    self.assertRaises(ValueError, hs110.receive, 123)
    self.assertRaises(ValueError, hs110.receive, 1.1)
    self.assertRaises(ValueError, hs110.receive, 3j)
    self.assertRaises(ValueError, hs110.receive, sample_data_fail)
    hs110.receive(sample_data_ok)
    hs110.receive(sample_data_h2)


  def test_constructor(self):
    h1_empty_print = 'current=0, voltage=0, power=0, total=0, err_code=0'
    h1_empty = {
      "emeter": {
        "get_realtime": {
          "current": 0,
          "voltage": 0,
          "power": 0,
          "total": 0,
          "err_code": 0
        }
      }
    }

    h2_empty_print = 'current_ma=0, voltage_mv=0, power_mw=0, total_wh=0, err_code=0'
    h2_empty = {
      "emeter": {
        "get_realtime": {
          "current_ma": 0,
          "voltage_mv": 0,
          "power_mw": 0,
          "total_wh": 0,
          "err_code": 0
        }
      }
    }

    self.assertRaises(ValueError, HS110data, hardware_version='h999')

    hs110 = HS110data('h1')
    self.assertEqual(hs110._HS110data__hardware, 'h1')
    self.assertEqual(hs110._HS110data__received_data, h1_empty)
    self.assertEqual(str(hs110), h1_empty_print)

    hs110 = HS110data('h2')
    self.assertEqual(hs110._HS110data__hardware, 'h2')
    self.assertEqual(hs110._HS110data__received_data, h2_empty)
    self.assertEqual(str(hs110), h2_empty_print)

    hs110 = HS110data()
    self.assertEqual(hs110._HS110data__hardware, 'h2')

    hs110._HS110data__received_data['emeter']['get_realtime']['current_ma'] = 1
    hs110._HS110data__received_data['emeter']['get_realtime']['voltate_mv'] = 220
    hs110._HS110data__received_data['emeter']['get_realtime']['power_mw'] = 220
    hs110._HS110data__received_data['emeter']['get_realtime']['total_wh'] = 1.3
    hs110._HS110data__received_data['emeter']['get_realtime']['err_code'] = 1
    hs110.reset_data()
    self.assertEqual(hs110._HS110data__received_data, h2_empty)

  def test_get_cmd(self):
    cmd_encrypted = b'\x00\x00\x00\x1e\xd0\xf2\x97\xfa\x9f\xeb\x8e\xfc\xde\xe4\x9f\xbd\xda\xbf\xcb\x94\xe6\x83\xe2\x8e\xfa\x93\xfe\x9b\xb9\x83\xf8\x85\xf8\x85'
    hs110 = HS110data()

    self.assertEqual(hs110.get_cmd(), cmd_encrypted)

if __name__ == '__main__':
    unittest.main()