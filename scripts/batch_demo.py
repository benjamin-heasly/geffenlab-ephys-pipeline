from run_pipeline import main

# List all the sessions to process.
# Each session gets a tuple of (experimenter, subject, date, ecephys_session_name).
sessions = [
    ("BH", "AS20-minimal3", "03112025", "AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0"),
    ("BH", "AS20-minimal3", "03112025", "another_session_test_g0"),
]

# Collect any exceptions so we can report them at the end.
exceptions = []

print(f"Starting batch of {len(sessions)} sessions:")
print(sessions)

for (experimenter, subject, date, ecephys_session_name) in sessions:

    print("\n")
    print(f"Starting session: {experimenter}, {subject}, {date}, {ecephys_session_name}")

    try:
        # Run the AIND ephys sorting pipeline on a minimal dataset, as in docs/run-aind-ephys-pipeline.md.
        aind_ephys_args = [
            "--workflow", "aind-ephys-pipeline/pipeline/main_multi_backend.nf",
            "--config", "geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config",
            "--experimenter", experimenter,
            "--subject", subject,
            "--date", date,
            "--input", "spikeglx",
            "--ecephys-session-name", ecephys_session_name,
            "-resume"
        ]
        main(aind_ephys_args)

        # Run the Geffen lab Phy export pipeline on the same dataset, as in docs/run-phy-export.md.
        phy_export_args = [
            "--workflow", "geffenlab-ephys-pipeline/phy-export/phy-export.nf",
            "--config", "geffenlab-ephys-pipeline/phy-export/cortex.config",
            "--experimenter", experimenter,
            "--subject", subject,
            "--date", date,
            "--input", "spikeglx",
            "--ecephys-session-name", ecephys_session_name,
            "-resume"
        ]
        main(phy_export_args)

    except Exception as exception:
        exceptions.append((experimenter, subject, date, ecephys_session_name, exception))
        print(f"Collected exception for {experimenter}, {subject}, {date}, {ecephys_session_name}:")
        print(exception)

print("\n")
print(f"Finished batch of {len(sessions)} sessions with {len(exceptions)} exceptions.")

for (experimenter, subject, date, ecephys_session_name, exception) in exceptions:
    print("\n")
    print(f"Had exception for {experimenter}, {subject}, {date}, {ecephys_session_name}:")
    print(exception)
