from bs4 import BeautifulSoup
from threading import Thread, Lock
from queue import Queue
import requests


class WebCrawler:
    def __init__(self, start_url: str, max_urls: int = 100, max_queue_size: int = 50):
        self.visited_urls = set([start_url])
        self.visited_lock = Lock()

        # backpressure (This will be useful in the scenario where producer is proucing at a very fast pace but consumer doesn't consume message at that pace)
        self.queue = Queue(maxsize=max_queue_size)
        self.queue.put(start_url)

        self.max_urls = max_urls
        self.total_crawled = 1

    def crawl(self):
        while True:
            url = self.queue.get()

            if url is None:  # sentinel → exit
                self.queue.task_done()
                return

            next_urls = self.get_next_urls(url)

            next_urls_to_add_into_queue=[]

            with self.visited_lock:
                print(f"Next Url for url - {url} is {len(next_urls)}, Total Crawled: {self.total_crawled}, Remaining: {self.max_urls-self.total_crawled}")
                for next_url in next_urls:
                    if self.total_crawled >= self.max_urls:
                        break  # stop producing new work

                    if next_url not in self.visited_urls:
                        self.visited_urls.add(next_url)
                        # blocks if full (helps in acieving backpressure), Don't do this because if the this thread blocks because we hit the max queue maxsize. But when other thread try to add in the queue, then they won't be able to do this because the lock has not released by this thread, So deadlock will be there (If wanted to have the backpressure then we will add these url outside of the loop, like we are doing here using next_urls_to_add_into_queue)
                        # self.queue.put(next_url)

                        # Instead add in a list and outside of the lock we will add those back into the queue
                        next_urls_to_add_into_queue.append(next_url)
                        self.total_crawled += 1

            # # Now add the urls present in the next_urls_to_add_into_queue, with blocking put for backpressure
            for next_url in next_urls_to_add_into_queue:
                self.queue.put(next_url)

            self.queue.task_done()

    def get_next_urls(self, url: str):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            return [a.get("href") for a in soup.find_all("a", href=True)]
        except Exception:
            return []

    def run(self, num_threads=10):
        threads = [Thread(target=self.crawl) for _ in range(num_threads)]

        for t in threads:
            t.start()

        # Blocks until all items in the Queue have been gotten and processed
        # i.e it will get blocked till we put all the actual urls (not the sentinal one), and those get processed
        # once we hit the threshold then our worker threads will block on queue.get()
        # But since all of the taks which were assigned to the queue got completed then at that timeout
        # This self.queue.join() will get executed and unblocked
        self.queue.join()

        print(f"Crawled all {self.max_urls} urls, Proceeding for Sentinal process.")

        # At this point, all of our threads will be waiting at .get() blocking call
        # send sentinel to stop all workers
        for _ in range(num_threads):
            self.queue.put(None)

        # Wait for all working thread to complete
        for t in threads:
            t.join()

        return self.visited_urls


if __name__ == "__main__":
    crawler = WebCrawler("https://www.youtube.com", max_urls=100, max_queue_size=50)
    result = crawler.run(num_threads=10)

    print(f"\nCrawled {len(result)} URLs\n")
