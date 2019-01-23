import io, os, zipfile
import requests

from bs4 import BeautifulSoup


class ImgTranslateTask(object):
    BASE_DIR = os.getcwd()
    DOWNLOAD_LINK = "http://staging.imgtranslate.com:9999/"

    def __init__(self):
        pass

    def fetch_urls(self):
        """Fetches the links in the url: DOWNLOAD_LINK 
		and adds the absolute path of online files to a class variable: download_urls

		Args:
		Returns:
		Raises:
		"""

        res = requests.get(self.DOWNLOAD_LINK)
        soup = BeautifulSoup(res.content, "lxml")

        hrefs = []
        for anchor in soup.find_all("a"):
            link = anchor.get("href")
            if link and link.strip("/"):
                hrefs.append(link.strip("/"))

        self.download_urls = ["{}{}".format(self.DOWNLOAD_LINK, path) for path in hrefs]

    def download_extract_files(self):
        """Downloads and extracts the files
		
		Args:
		Returns:
		Raises	
		"""
        for url in self.download_urls:
            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()

    def find_files(self):
        """Finds all the extracted files	

		Args:
		Returns:
		Raises:
		"""
        self.files_path = []
        for dirpath, _, filenames in os.walk(self.BASE_DIR):
            files = [f for f in filenames if f.endswith(".txt")]
            for filename in files:
                self.files_path.append(
                    os.path.join(self.BASE_DIR, os.path.join(dirpath, filename))
                )

    def compare_and_print_output(self):
        """Compares the files for duplicate lines and prints the output
		
		Args:
		Returns:
		Raises:
		 """
        for i in range(0, len(self.files_path)):
            with open(self.files_path[i]) as f:
                s1 = set(line.strip() for line in f.readlines())
            for j in range(i + 1, len(self.files_path)):
                with open(self.files_path[j]) as f:
                    s2 = set(line.strip() for line in f.readlines())

                    # Compare two files for common lines
                intersection = s1 & s2

                if len(intersection) > 2:
                    file1 = os.path.split(self.files_path[i])[-1]
                    file2 = os.path.split(self.files_path[j])[-1]
                    print(file1, file2)

    def run(self):
        self.fetch_urls()
        self.download_extract_files()
        self.find_files()
        self.compare_and_print_output()


def main():
    base_dir = os.getcwd()
    os.chdir(base_dir)
    ImgTranslateTask().run()


if __name__ == "__main__":
    main()
