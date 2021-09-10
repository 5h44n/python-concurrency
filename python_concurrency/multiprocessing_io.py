import requests
import multiprocessing
import time

session = None

# each process gets a session stored as a global var in memory
def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}: Read {len(response.content)} from {url}")

# using `initializer` argument, each process gets a `Session` object stored as a global var in memory, persisting between function calls
def download_all_sites(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)


def main():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"\nDownloaded {len(sites)} in {duration} seconds\n")


if __name__ == "__main__":
    main()
