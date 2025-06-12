#!/usr/bin/env nextflow
// hash:sha256:78ed200fe64a9c464b9cf5339667b94f5a7f28844e7b4f088d44927775f7dadb

// capsule - geffenlab-ecephys-phy-export
process capsule_geffenlab_ecephys_phy_export_1 {
	tag 'capsule-3318936'
	container "$REGISTRY_HOST/capsule/dfa653e1-1168-413f-989a-53c75f848b58:f20535eb0428df68f53002718f3e88e1"

	cpus 4
	memory '30 GB'

	publishDir "$RESULTS_PATH", saveAs: { filename -> new File(filename).getName() }

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

	ln -s "/tmp/data/ecephys" "capsule/data/ecephys" # id: 2429fd9e-80c5-4cf0-a281-9c8043cfc402
	ln -s "/tmp/data/ecephys_AS20_2025-03-11_11-08-51_v2_sorted" "capsule/data/ecephys_AS20_2025-03-11_11-08-51_v2_sorted" # id: 7603f7a9-14d8-4274-9d63-e39a58c31413

	echo "[${task.tag}] cloning git repo..."
	if [[ "\$(printf '%s\n' "2.20.0" "\$(git version | awk '{print \$3}')" | sort -V | head -n1)" = "2.20.0" ]]; then
		git clone --filter=tree:0 "https://\$GIT_ACCESS_TOKEN@\$GIT_HOST/capsule-3318936.git" capsule-repo
	else
		git clone "https://\$GIT_ACCESS_TOKEN@\$GIT_HOST/capsule-3318936.git" capsule-repo
	fi
	git -C capsule-repo checkout c50c2cc430ddf10e7798a4aba30b2418088b293d --quiet
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
	// run processes
	capsule_geffenlab_ecephys_phy_export_1()
}
