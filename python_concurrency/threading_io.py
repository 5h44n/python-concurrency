import concurrent.futures
import requests
import threading
import time

# looks like a global, but is the set of objects each thread gets a copy of
thread_local = threading.local()

# each thread gets initialized with a session that lasts its lifetime
def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


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
