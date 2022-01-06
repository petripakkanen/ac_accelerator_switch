import unittest

# from aclSignal.aclSignal import AclSignalPoint
from aclSignal.aclSignal import AclSignalPoint, AclSignalGroup

test_points = [435362346252, 0.43154325562, 0.2345243524, 0.234526256]


class SimpleTest(unittest.TestCase):
    #   def testadd1(self):
    #      self.assertEquals(add(4,5),'{9')

    def __init__(self, *args):
        super().__init__(*args)
        self.aclsp = AclSignalPoint(
            test_points[0], test_points[1], test_points[2], test_points[3]
        )
        self.sclsg = AclSignalGroup(self.aclsp)

    def test_single_construct(self):
        self.assertEqual(self.aclsp.timestamp_ns, test_points[0])
        self.assertEqual(self.aclsp.acc_x, test_points[1] / self.aclsp.g_div)
        self.assertEqual(self.aclsp.acc_y, test_points[2] / self.aclsp.g_div)
        self.assertEqual(self.aclsp.acc_z, test_points[3] / self.aclsp.g_div)

    def test_group_construct(self):
        assert self.sclsg

        # 	def test_AclSignalPoint_constructor(self):


# 		self.assertEquals(AclSignalPoint())

if __name__ == "__main__":
    unittest.main()
