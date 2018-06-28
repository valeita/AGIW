import json
import os
import sys



WRAPPER_1 = {"name" : "spexa", "dir_path" : "/Users/Valerio/Desktop/output"}
WRAPPER_2 = {"name" : "xpathmen", "dir_path" : "/Users/Valerio/Desktop/Extracted_data"}



def print_wrappers_stats(wrappers_stats) :

	print("*** WRAPPERS STATS ***\n")
	print("the wrapper values are the number of domains per percentual range of non-empty extracted jsons\n")

	print("non-empty", end='')

	for wrapper_name in wrappers_stats :

		print("\t" + wrapper_name, end='')

	print('\n')

	w1_id, w2_id = wrappers_stats.keys()

	w1 = wrappers_stats[w1_id]
	w2 = wrappers_stats[w2_id]

	for interval in get_intervals() :

		print(interval + " : \t", end='')
		print(str(w1[interval]) + "\t", end='')
		print(str(w2[interval]) + "\n\n")



def print_domain_stats(domain, domain_stats) :

	w1_stats = domain_stats[WRAPPER_1["name"]]
	w2_stats = domain_stats[WRAPPER_2["name"]]

	print("=== " + domain + " ===\n")
	print("\t" + WRAPPER_1["name"] + " :\n\t", end='')
	print(w1_stats)
	print("\t" + WRAPPER_2["name"] + " :\n\t", end='')
	print(w2_stats)
	print("\n")



def update_wrapper_stats(wrapper_stats, domain_stats) :

	lower_bound = int(domain_stats["non_empty_perc"] // 10) * 10

	if lower_bound == 0 :

		interval = "0-10%"

	elif lower_bound == 100 :

		interval = "90-100%"

	else :

		upper_bound = lower_bound + 10
		interval = str(lower_bound) + "-" + str(upper_bound) + "%"

	wrapper_stats[interval] += 1



def get_json_specs_count(json_file_path) :

	with open(json_file_path) as j :

		try :

			loaded_specs = json.load(j)

		except json.JSONDecodeError :

			loaded_specs = {}

	specs = loaded_specs

	if type(loaded_specs) == list :

		specs = loaded_specs[0]

	return len(specs.keys())



def get_domain_stats(domain_dir_path) :

	non_empty_json_count = 0
	domain_specs_count = 0

	json_files = [f for f in os.listdir(domain_dir_path) if f.endswith(".json")]
	json_files_count = len(json_files)

	for json_file in json_files :

		json_file_path = os.path.join(domain_dir_path, json_file)
		json_specs_count = get_json_specs_count(json_file_path)

		domain_specs_count += json_specs_count
		non_empty_json_count += 1 if json_specs_count > 0 else 0

	non_empty_json_percentual = 0
	domain_specs_avg = 0

	if(non_empty_json_count > 0) :

		non_empty_json_percentual = non_empty_json_count * 100 / json_files_count
		domain_specs_avg = domain_specs_count / non_empty_json_count

	return \
	{
		"non_empty_perc" : round(non_empty_json_percentual, 2),
		"domain_specs_avg" : round(domain_specs_avg, 2)
	}



def get_domains_in_common() :

	w1_domains = os.listdir(WRAPPER_1["dir_path"])
	w2_domains = os.listdir(WRAPPER_2["dir_path"])

	domains_in_common = \
		list(set(w1_domains).intersection(set(w2_domains)))

	domains_in_common.sort()

	return domains_in_common



def get_intervals() :

	return \
	[
		"0-10%",
		"10-20%",
		"20-30%",
		"30-40%",
		"40-50%",
		"50-60%",
		"60-70%",
		"70-80%",
		"80-90%",
		"90-100%"
	]



def initialize_wrappers_stats(wrappers_stats) :

	wrappers_stats[WRAPPER_1["name"]] = {}
	wrappers_stats[WRAPPER_2["name"]] = {}

	for wrapper in [WRAPPER_1, WRAPPER_2] :

		for interval in get_intervals() :

			wrappers_stats[wrapper['name']][interval] = 0



def print_wrapper_dir_is_invalid(wrapper) :

		sys.stderr.write(
		"Error : " +
		wrapper["name"] +
		"'s output directory is invalid!\n(" +
		wrapper["dir_path"] +
		")\n\n"
		)



def is_wrapper_dir_valid(wrapper) :

	wrapper_dir_path = wrapper["dir_path"]

	return os.path.isdir(wrapper_dir_path) and \
	os.listdir(wrapper_dir_path) is not []



def check_wrappers_dirs() :

	are_wrapper_dirs_valid = True

	for wrapper in [WRAPPER_1, WRAPPER_2] :

		if not is_wrapper_dir_valid(wrapper) :

			print_wrapper_dir_is_invalid(wrapper)
			are_wrapper_dirs_valid = False

	if not are_wrapper_dirs_valid :

		exit(1)



def main() :

	check_wrappers_dirs()

	wrappers_stats = {}
	initialize_wrappers_stats(wrappers_stats)

	for domain in get_domains_in_common() :

		domain_stats = {}

		for wrapper in [WRAPPER_1, WRAPPER_2] :

			w_name = wrapper["name"]
			domain_dir_path = os.path.join(wrapper["dir_path"], domain)

			domain_stats[w_name] = get_domain_stats(domain_dir_path)

			update_wrapper_stats(wrappers_stats[w_name], domain_stats[w_name])

		print_domain_stats(domain, domain_stats)

	print_wrappers_stats(wrappers_stats)



if __name__ == "__main__" :

	main()