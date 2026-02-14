import unittest

class TestMain(unittest.TestCase):

    def test_create_download_dir(self):
        from main import create_downloads_directory
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmp_dir:
            downloads_dir = create_downloads_directory(tmp_dir)
            self.assertTrue(os.path.exists(downloads_dir))
            self.assertEqual(downloads_dir, os.path.join(tmp_dir, "downloads"))

    def test_is_reachable_uri(self):
        from main import is_reachable_uri
        
        self.assertTrue(is_reachable_uri("https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip"))
        self.assertFalse(is_reachable_uri("https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip"))
        self.assertFalse(is_reachable_uri("https://example.com/nonexistentfile.zip"))

    def test_download_from_uri(self):
        from main import download_from_uri
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = os.path.join(tmp_dir, "downloads")
            os.makedirs(out_dir)

            # Test downloading a valid file
            download_from_uri("https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip", out_dir)
            self.assertTrue(os.path.exists(os.path.join(out_dir, "Divvy_Trips_2020_Q1.zip")))

            # Test downloading an invalid file (should not raise an exception)
            download_from_uri("https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip", out_dir)
            self.assertFalse(os.path.exists(os.path.join(out_dir, "Divvy_Trips_2220_Q1.zip")))

    def test_unzip_file(self):
        from main import unzip_file
        import tempfile
        import os
        import zipfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create a sample zip file
            zip_path = os.path.join(tmp_dir, "test.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.writestr("test.txt", "This is a test file.")

            # Unzip the file
            unzip_file(zip_path)

            # Check that the unzipped file exists and has the correct content
            unzipped_file_path = os.path.join(tmp_dir, "test.txt")
            self.assertTrue(os.path.exists(unzipped_file_path))
            with open(unzipped_file_path, 'r') as f:
                content = f.read()
                self.assertEqual(content, "This is a test file.")

    def test_download_and_unzip_from_uri(self):
        from main import download_and_unzip_from_uri
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = os.path.join(tmp_dir, "downloads")
            os.makedirs(out_dir)

            # Test downloading and unzipping a valid file
            download_and_unzip_from_uri("https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip", out_dir)
            self.assertTrue(os.path.exists(os.path.join(out_dir, "Divvy_Trips_2020_Q1.csv")))

            # Test downloading and unzipping an invalid file (should not raise an exception)
            download_and_unzip_from_uri("https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip", out_dir)
            self.assertFalse(os.path.exists(os.path.join(out_dir, "Divvy_Trips_2220_Q1.csv")))

    def test_download_and_unzip_from_uris(self):
        from main import download_and_unzip_from_uris
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = os.path.join(tmp_dir, "downloads")
            os.makedirs(out_dir)

            uris = [
                "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
                "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip"
            ]

            download_and_unzip_from_uris(uris, out_dir)

            self.assertTrue(os.path.exists(os.path.join(out_dir, "Divvy_Trips_2020_Q1.csv")))
            self.assertFalse(os.path.exists(os.path.join(out_dir, "Divvy_Trips_2220_Q1.csv")))

if __name__ == '__main__':
    unittest.main()
