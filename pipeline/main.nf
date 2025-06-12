#!/usr/bin/env nextflow
// hash:sha256:e4bcaed923803c9dfde289f13e55aa35f64dae47092e794f895eddd93c080d8d

// capsule - geffenlab-ecephys-phy-export
process capsule_geffenlab_ecephys_phy_export_1 {
	tag 'capsule-3318936'
	container "$REGISTRY_HOST/capsule/dfa653e1-1168-413f-989a-53c75f848b58"

	cpus 4
	memory '30 GB'

	publishDir "$RESULTS_PATH", saveAs: { filename -> new File(filename).getName() }

	input:
	val path1

	output:
	path 'capsule/results/*'

	script:
	"""
	#!/usr/bin/env bash
	set -e

	export CO_CAPSULE_ID=dfa653e1-1168-413f-989a-53c75f848b58
	export CO_CPUS=4
	export CO_MEMORY=32212254720

	mkdir -p capsule
	mkdir -p capsule/data && ln -s \$PWD/capsule/data /data
	mkdir -p capsule/results && ln -s \$PWD/capsule/results /results
	mkdir -p capsule/scratch && ln -s \$PWD/capsule/scratch /scratch

	ln -s "/tmp/data/ecephys_AS20_2025-03-11_11-08-51_v2_sorted/$path1" "capsule/data/$path1" # id: 7603f7a9-14d8-4274-9d63-e39a58c31413

	echo "[${task.tag}] cloning git repo..."
	if [[ "\$(printf '%s\n' "2.20.0" "\$(git version | awk '{print \$3}')" | sort -V | head -n1)" = "2.20.0" ]]; then
		git clone --filter=tree:0 "https://\$GIT_ACCESS_TOKEN@\$GIT_HOST/capsule-3318936.git" capsule-repo
	else
		git clone "https://\$GIT_ACCESS_TOKEN@\$GIT_HOST/capsule-3318936.git" capsule-repo
	fi
	mv capsule-repo/code capsule/code
	rm -rf capsule-repo

	echo "[${task.tag}] running capsule..."
	cd capsule/code
	chmod +x run
	./run ${params.capsule_geffenlab_ecephys_phy_export_1_args}

	echo "[${task.tag}] completed!"
	"""
}

workflow {
	// input data
	ecephys_as20_2025_03_11_11_08_51_v2_sorted_to_geffenlab_ecephys_phy_export_1 = Channel.fromPath("../data/ecephys_AS20_2025-03-11_11-08-51_v2_sorted/*", type: 'any', relative: true)

	// run processes
	capsule_geffenlab_ecephys_phy_export_1(ecephys_as20_2025_03_11_11_08_51_v2_sorted_to_geffenlab_ecephys_phy_export_1)
}
