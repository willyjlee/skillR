# parsed_a
# parsed_b
# parsed_a and parsed_b are lists of dictionaries
# each dictionary represents a frame
# each dictionary value is of form 0: ((a, b), c)
# this means body part 0 is at coordinate (a, b) with score c

# assumes that both parsed values have been scaled time-wise and
# have the same or similar number of frames

# let a be the reference

# only use bodyparts that are in both


index_to_bodypart = { 0:  "Nose", 1:  "Neck", 2:  "RShoulder", 3:  "RElbow", 4:  "RWrist", 5:  "LShoulder", 6:  "LElbow", 7:  "LWrist", 8:  "RHip", 9:  "RKnee", 10: "RAnkle", 11: "LHip", 12: "LKnee", 13: "LAnkle", 14: "REye" }

def parse(file):
    fd = open(file, 'r')
    lines = [line.rstrip() for line in fd.readlines()]
    parsed = []
    cur = {}
    for line in lines:
        if line.split(' ')[0] == 'frame':
            parsed.append(cur)
            cur = {}
        else:
            cur[int(line[9:line.find('-')])] = [[float(line[line.find('(')+1 : line.find(',')]), float(line[line.find(',')+2 : line.find(')')])], float(line.split(' ')[2][6:])]
    return parsed[1:]




def ave(inp):
    for ind, frame in enumerate(inp):
        for part in range(18):
            if part in [14, 15, 16, 17]:
                continue
            if part not in frame:
                left = [x for x in inp[:ind] if part in x]
                right = [x for x in inp[ind + 1:] if part in x]
                if (not left) and (not right):
                    print(ind)
                    print('oh no brh')
                    return
                ((x,y), s) = ((0.,0.),0.)

                cnt = 0
                if left:
                    ((lx, ly), ls) = left[-1][part]
                    x += lx
                    y += ly
                    s += ls
                    cnt += 1
                if right:
                    ((rx, ry), rs) = right[0][part]
                    x += rx
                    y += ry
                    s += rs
                    cnt += 1
                x /= cnt
                y /= cnt
                s /= cnt
                frame[part] = [[x, y], s]
    return inp

parsed_a = ave(parse('willy1.txt'))
parsed_b = ave(parse('willy2.txt'))

# print(parsed_a)

bodypart_indices_a = list(range(14))
bodypart_indices_b = list(range(14))

frame = parsed_a[0]
for bodypart_index in range(14):
	if bodypart_index not in frame:
		bodypart_indices_a.remove(bodypart_index)

frame = parsed_b[0]
for bodypart_index in range(14):
	if bodypart_index not in frame:
		bodypart_indices_b.remove(bodypart_index)

bodypart_indices = [value for value in bodypart_indices_a if value in bodypart_indices_b]


#center around torso
for frame in parsed_a:
	offset = frame[1][0]
	offset_x = offset[0]
	offset_y = offset[1]
	for bodypart_index in bodypart_indices:
		frame[bodypart_index][0][0] -= offset_x
		frame[bodypart_index][0][1] -= offset_y

for frame in parsed_b:
	offset = frame[1][0]
	offset_x = offset[0]
	offset_y = offset[1]
	for bodypart_index in bodypart_indices:
		frame[bodypart_index][0][0] -= offset_x
		frame[bodypart_index][0][1] -= offset_y

# max values
top_a = -1
bottom_a = 1
left_a = 1
right_a = -1

top_b = -1
bottom_b = 1
left_b = 1
right_b = -1

for frame in parsed_a:
	for bodypart_index in bodypart_indices:
		data = frame[bodypart_index]
		coord = data[0]
		x = coord[0]
		y = coord[1]
		if y > top_a:
			top_a = y
		if y < bottom_a:
			bottom_a = y
		if x < left_a:
			left_a = x
		if x > right_a:
			right_a = x

for frame in parsed_b:
	for bodypart_index in bodypart_indices:
		data = frame[bodypart_index]
		coord = data[0]
		x = coord[0]
		y = coord[1]
		if y > top_b:
			top_b = y
		if y < bottom_b:
			bottom_b = y
		if x < left_b:
			left_b = x
		if x > right_b:
			right_b = x

# scaling
for frame in parsed_a:
	for bodypart_index in bodypart_indices:
		data = frame[bodypart_index]
		coord = data[0]
		x = coord[0]
		y = coord[1]
		if y > 0:
			y = y / top_a
		else:
			y = y / bottom_a
		if x > 0:
			x = x / right_a
		else:
			x = x / left_a

for frame in parsed_b:
	for bodypart_index in bodypart_indices:
		data = frame[bodypart_index]
		coord = data[0]
		x = coord[0]
		y = coord[1]
		if y > 0:
			y = y / top_b
		else:
			y = y / bottom_b
		if x > 0:
			x = x / right_b
		else:
			x = x / left_b


#compare
offsets = [[] for bodypart in bodypart_indices]
# scores = [[] for bodypart in bodypart_indices]

for frame_index in range(min(len(parsed_a), len(parsed_b))):
	frame_a = parsed_a[frame_index]
	frame_b = parsed_b[frame_index]
	for i in range(len(bodypart_indices)):
		data_a = frame_a[bodypart_indices[i]]
		data_b = frame_b[bodypart_indices[i]]
		coord_a = data_a[0]
		coord_b = data_b[0]
		offset_x = coord_b[0] - coord_a[0]
		offset_y = coord_b[1] - coord_a[1]
		offset = [offset_x, offset_y]
		offsets[i].append(offset)


for bodypart_offsets in offsets:
	avg_x_offset = sum([x[0] for x in bodypart_offsets]) / len(bodypart_offsets)
	avg_y_offset = sum([y[0] for y in bodypart_offsets]) / len(bodypart_offsets)
	print(round(avg_x_offset, 3), round(avg_y_offset, 3))