import numpy as np
import pandas as pd

from skmob.core.trajectorydataframe import TrajDataFrame
from skmob.preprocessing import detection
from skmob.utils import constants


class TestDetection:
    def setup_method(self):
        latitude = constants.LATITUDE
        longitude = constants.LONGITUDE
        date_time = constants.DATETIME
        user_id = constants.UID

        lat_lons = np.array(
            [
                [43.8430139, 10.5079940],
                [43.5442700, 10.3261500],
                [43.7085300, 10.4036000],
                [43.7792500, 11.2462600],
                [43.8430139, 10.5079940],
                [43.7085300, 10.4036000],
                [43.8430139, 10.5079940],
                [43.5442700, 10.3261500],
                [43.5442700, 10.3261500],
                [43.7085300, 10.4036000],
                [43.8430139, 10.5079940],
                [43.7792500, 11.2462600],
                [43.7085300, 10.4036000],
                [43.5442700, 10.3261500],
                [43.7792500, 11.2462600],
                [43.7085300, 10.4036000],
                [43.7792500, 11.2462600],
                [43.8430139, 10.5079940],
                [43.8430139, 10.5079940],
                [43.5442700, 10.3261500],
                [45.5442700, 9.3261500],
                [45.5442700, 9.3261500],
                [45.5442700, 9.3261500],
            ]
        )

        traj = pd.DataFrame(lat_lons, columns=[latitude, longitude])

        traj[date_time] = pd.to_datetime(
            [
                "20110203 8:34:04",
                "20110203 9:34:04",
                "20110203 10:34:04",
                "20110204 10:34:04",
                "20110203 8:34:04",
                "20110203 9:34:04",
                "20110204 10:34:04",
                "20110204 11:34:04",
                "20110203 8:34:04",
                "20110203 9:34:04",
                "20110204 10:34:04",
                "20110204 11:34:04",
                "20110204 10:34:04",
                "20110204 11:34:04",
                "20110204 12:34:04",
                "20110204 10:34:04",
                "20110204 11:34:04",
                "20110205 12:34:04",
                "20110204 10:34:04",
                "20110204 11:34:04",
                "20110204 11:34:04", 
                "20110205 11:34:04", 
                "20110206 11:34:04",
            ]
        )

        traj[user_id] = (
            [1 for _ in range(4)]
            + [2 for _ in range(4)]
            + [3 for _ in range(4)]
            + [4 for _ in range(3)]
            + [5 for _ in range(3)]
            + [6 for _ in range(2)]
            + [7 for _ in range(3)]
        )

        self.unique_points = [
            (43.544270, 10.326150),
            (43.708530, 10.403600),
            (43.779250, 11.246260),
            (43.843014, 10.507994),
        ]

        self.traj = traj.sort_values([user_id, date_time])
        self.trjdat = TrajDataFrame(traj, user_id=user_id)

    def test_stops(self):
        output = detection.stops(self.trjdat)

        expected = self.trjdat.drop([3, 7, 11, 14, 17, 19, 21, 22])
        stamps = [
            pd.Timestamp("2011-02-03 09:34:04"),
            pd.Timestamp("2011-02-03 10:34:04"),
            pd.Timestamp("2011-02-04 10:34:04"),
            pd.Timestamp("2011-02-03 09:34:04"),
            pd.Timestamp("2011-02-04 10:34:04"),
            pd.Timestamp("2011-02-04 11:34:04"),
            pd.Timestamp("2011-02-03 09:34:04"),
            pd.Timestamp("2011-02-04 10:34:04"),
            pd.Timestamp("2011-02-04 11:34:04"),
            pd.Timestamp("2011-02-04 11:34:04"),
            pd.Timestamp("2011-02-04 12:34:04"),
            pd.Timestamp("2011-02-04 11:34:04"),
            pd.Timestamp("2011-02-05 12:34:04"),
            pd.Timestamp("2011-02-04 11:34:04"),
            pd.Timestamp('2011-02-06 11:34:04')
        ]

        expected["leaving_datetime"] = stamps

        output.reset_index(inplace=True)
        output.drop(columns=["index"], inplace=True)

        expected.reset_index(inplace=True)
        expected.drop(columns=["index"], inplace=True)

        # assert
        pd.testing.assert_frame_equal(output, expected, check_dtype=False)

        output = detection.stops(self.trjdat, minutes_for_a_stop=60.0, leaving_time=False)

        expected = self.trjdat.drop([0, 1, 3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22])

        output.reset_index(inplace=True)
        output.drop(columns=["index"], inplace=True)

        expected.reset_index(inplace=True)
        expected.drop(columns=["index"], inplace=True)

        # assert
        pd.testing.assert_frame_equal(output, expected, check_dtype=False)
