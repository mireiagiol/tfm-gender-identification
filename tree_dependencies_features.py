height_counter = 0
child_width_counter = 0
subchild_width_counter = 0
counters = []


def parse_json(json_data):
    results = []
    for sentence in json_data.get('sentences'):
        parse_sentence(sentence)
        global height_counter
        global counters
        global child_width_counter
        global subchild_width_counter
        results.append([len(json_data.get('sentences')), max(counters, default=0), height_counter])
        height_counter = 0
        counters = []
        child_width_counter = 0
        subchild_width_counter = 0
    return results


def parse_sentence(sentence):
    dependency = sentence.get('dependencies')[0]
    if dependency.get('children') is not None:
        global height_counter
        height_counter = height_counter + 1
        for child in dependency.get('children'):
            global child_width_counter
            child_width_counter += 1
            parse_child(child)
        counters.append(child_width_counter)


def parse_child(child):
    if child.get('children') is not None:
        global height_counter
        height_counter = height_counter + 1
        for subchild in child.get('children'):
            global subchild_width_counter
            subchild_width_counter += 1
            parse_child(subchild)
        counters.append(subchild_width_counter)