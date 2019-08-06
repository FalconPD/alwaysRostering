import csv
import os.path
import logging

class ID_Map():
    # Two dicts to make lookups quick
    genesis_to_atlas = {}
    atlas_to_genesis = {}
    map_file = None

    def __init__(self, map_file):
        """
        Reads the CSV file that saves our ID map. CSV file should be:
        genesis_id,atlas_id
        <genesis_id>,<atlas_id>
        ...
        """
        self.map_file = map_file
        # if the file doesn't exist we'll create it on save()
        if os.path.isfile(map_file):
            with open(self.map_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) # Skip the header
                for row in reader:
                    self.genesis_to_atlas[row[0]] = row[1]
                    self.atlas_to_genesis[row[1]] = row[0]

    def add(self, genesis_id, atlas_id):
        """
        Adds an ID pair.
        """
        self.genesis_to_atlas[genesis_id] = atlas_id
        self.atlas_to_genesis[atlas_id] = genesis_id

    def get_atlas(self, genesis_id):
        """
        Gets the genesis_id for an atlas_id or '' if
        it can't be found
        """
        if genesis_id not in self.genesis_to_atlas:
            logging.warning("Unable to map Genesis ID {} to an Atlas ID".format(
                genesis_id))
            return ''
        return self.genesis_to_atlas[genesis_id]

    def get_genesis(self, atlas_id):
        """
        Gets the atlas_id for an genesis_id or '' if
        it can't be found
        """
        if atlas_id not in self.atlas_to_genesis:
            logging.warning("Unable to map Atlas ID {} to a Genesis ID".format(
                atlas_id))
            return ''
        return self.atlas_to_genesis[atlas_id]

    def del_by_atlas(self, atlas_id):
        """
        Deletes the hash pair based on atlas_id
        """
        del self.genesis_to_atlas[self.atlas_to_genesis[atlas_id]]        
        del self.atlas_to_genesis[atlas_id]

    def save(self):
        """
        Saves the current ID map to a CSV file
        """
        with open(self.map_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['genesis_id','atlas_id'])
            for key in sorted(self.genesis_to_atlas.keys()):
                writer.writerow([key, self.genesis_to_atlas[key]])
