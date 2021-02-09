import sys
from corpus.CorpusCollector import CorpusCollector

if __name__ == '__main__':
    topic = sys.argv[1]

    collector = CorpusCollector(topic)
    old_dump = collector.get_dump_or_create_new()
    new_batch = collector.collect()
    new_dump = old_dump.append(new_batch)
    collector.dump(new_dump)