---
title: SpiNNaker cfg settings
layout: default
published: true
---
This guide covers the cfg settings and the reports created
* CFG Sections
  * [Logging](#Logging)
  * [Machine](#Machine)
  * [Database](#Database)
  * [Mapping](#Mapping)
  * [Reports](#Reports)
  * [Buffers](#Buffers)
  * [Mode](#Mode)
  * [EnergyMonitor](#EnergyMonitor)
  * [Java](#Java)
  * [Simulation](#Simulation)
  * [Recording](#Recording)
* [Report Files](#report_files)
# <a name="Logging"></a> Logging
This section controls the logger
* [default](#default)
* [instantiate](#instantiate)
### <a name="default"></a> default
Logging Level (in lower case) to be used.
* key: default 
* value: info
### <a name="instantiate"></a> instantiate
Determines if logging is done or not
* key: instantiate 
* value: True
# <a name="Machine"></a> Machine
This section controls getting a spinnaker machine
* [auto_detect_bmp](#auto_detect_bmp)
* [bmp_names](#bmp_names)
* [clear_routing_tables](#clear_routing_tables)
* [clear_tags](#clear_tags)
* [disable_advanced_monitor_usage_for_data_in](#disable_advanced_monitor_usage_for_data_in)
* [down_chips](#down_chips)
* [down_cores](#down_cores)
* [down_links](#down_links)
* [enable_advanced_monitor_support](#enable_advanced_monitor_support)
* [enable_reinjection](#enable_reinjection)
* [height](#height)
* [ignore_bad_ethernets](#ignore_bad_ethernets)
* [json_path](#json_path)
* [machine_name](#machine_name)
* [machine_spec_file](#machine_spec_file)
* [max_machine_core](#max_machine_core)
* [max_sdram_allowed_per_chip](#max_sdram_allowed_per_chip)
* [post_simulation_overrun_before_error](#post_simulation_overrun_before_error)
* [remote_spinnaker_url](#remote_spinnaker_url)
* [repair_machine](#repair_machine)
* [report_waiting_logs](#report_waiting_logs)
* [reset_machine_on_startup](#reset_machine_on_startup)
* [simulation_time_step](#simulation_time_step)
* [spalloc_avoid_boards](#spalloc_avoid_boards)
* [spalloc_group](#spalloc_group)
* [spalloc_machine](#spalloc_machine)
* [spalloc_port](#spalloc_port)
* [spalloc_server](#spalloc_server)
* [spalloc_use_proxy](#spalloc_use_proxy)
* [spalloc_user](#spalloc_user)
* [time_scale_factor](#time_scale_factor)
* [turn_off_machine](#turn_off_machine)
* [version](#version)
* [versions](#versions)
* [virtual_board](#virtual_board)
* [width](#width)
### <a name="auto_detect_bmp"></a> auto_detect_bmp
* key: auto_detect_bmp 
* value: False
### <a name="bmp_names"></a> bmp_names
* key: bmp_names 
* value: None
### <a name="clear_routing_tables"></a> clear_routing_tables
* key: clear_routing_tables 
* value: False
### <a name="clear_tags"></a> clear_tags
* key: clear_tags 
* value: False
### <a name="disable_advanced_monitor_usage_for_data_in"></a> disable_advanced_monitor_usage_for_data_in
* key: disable_advanced_monitor_usage_for_data_in 
* value: False
### <a name="down_chips"></a> down_chips
* key: down_chips 
* value: None
### <a name="down_cores"></a> down_cores
* key: down_cores 
* value: None
### <a name="down_links"></a> down_links
* key: down_links 
* value: None
### <a name="enable_advanced_monitor_support"></a> enable_advanced_monitor_support
* key: enable_advanced_monitor_support 
* value: True
### <a name="enable_reinjection"></a> enable_reinjection
* key: enable_reinjection 
* value: True
### <a name="height"></a> height
* key: height 
* value: None
### <a name="ignore_bad_ethernets"></a> ignore_bad_ethernets
* key: ignore_bad_ethernets 
* value: True
### <a name="json_path"></a> json_path
* key: json_path 
* value: None
### <a name="machine_name"></a> machine_name
* key: machine_name 
* value: None
### <a name="machine_spec_file"></a> machine_spec_file
This points to a second cfg file to read the machine details from
This allows for easily switching your configs between different baords and spalloc.
While designed for Machine settings can include any cfg setting. (Except another machine_spec_file)
* key: machine_spec_file 
* value: None
### <a name="max_machine_core"></a> max_machine_core
* key: max_machine_core 
* value: None
### <a name="max_sdram_allowed_per_chip"></a> max_sdram_allowed_per_chip
* key: max_sdram_allowed_per_chip 
* value: None
### <a name="post_simulation_overrun_before_error"></a> post_simulation_overrun_before_error
* key: post_simulation_overrun_before_error 
* value: 5
### <a name="remote_spinnaker_url"></a> remote_spinnaker_url
* key: remote_spinnaker_url 
* value: None
### <a name="repair_machine"></a> repair_machine
* key: repair_machine 
* value: False
### <a name="report_waiting_logs"></a> report_waiting_logs
* key: report_waiting_logs 
* value: False
### <a name="reset_machine_on_startup"></a> reset_machine_on_startup
* key: reset_machine_on_startup 
* value: False
### <a name="simulation_time_step"></a> simulation_time_step
* key: simulation_time_step 
* value: 1000
### <a name="spalloc_avoid_boards"></a> spalloc_avoid_boards
* key: spalloc_avoid_boards 
* value: None
### <a name="spalloc_group"></a> spalloc_group
* key: spalloc_group 
* value: None
### <a name="spalloc_machine"></a> spalloc_machine
* key: spalloc_machine 
* value: None
### <a name="spalloc_port"></a> spalloc_port
* key: spalloc_port 
* value: 22244
### <a name="spalloc_server"></a> spalloc_server
* key: spalloc_server 
* value: None
### <a name="spalloc_use_proxy"></a> spalloc_use_proxy
* key: spalloc_use_proxy 
* value: True
### <a name="spalloc_user"></a> spalloc_user
* key: spalloc_user 
* value: None
### <a name="time_scale_factor"></a> time_scale_factor
* key: time_scale_factor 
* value: None
### <a name="turn_off_machine"></a> turn_off_machine
* key: turn_off_machine 
* value: False
### <a name="version"></a> version
* key: version 
* value: None
### <a name="versions"></a> versions
* key: versions 
* value: None
### <a name="virtual_board"></a> virtual_board
* key: virtual_board 
* value: False
### <a name="width"></a> width
* key: width 
* value: None
# <a name="Database"></a> Database
* [create_database](#create_database)
* [create_routing_info_to_neuron_id_mapping](#create_routing_info_to_neuron_id_mapping)
* [listen_port](#listen_port)
* [notify_hostname](#notify_hostname)
* [notify_port](#notify_port)
* [wait_on_confirmation](#wait_on_confirmation)
* [wait_on_confirmation_timeout](#wait_on_confirmation_timeout)
### <a name="create_database"></a> create_database
* key: create_database 
* value: None
### <a name="create_routing_info_to_neuron_id_mapping"></a> create_routing_info_to_neuron_id_mapping
* key: create_routing_info_to_neuron_id_mapping 
* value: True
### <a name="listen_port"></a> listen_port
* key: listen_port 
* value: None
### <a name="notify_hostname"></a> notify_hostname
* key: notify_hostname 
* value: localhost
### <a name="notify_port"></a> notify_port
* key: notify_port 
* value: 19999
### <a name="wait_on_confirmation"></a> wait_on_confirmation
* key: wait_on_confirmation 
* value: True
### <a name="wait_on_confirmation_timeout"></a> wait_on_confirmation_timeout
* key: wait_on_confirmation_timeout 
* value: 10
# <a name="Mapping"></a> Mapping
* [compression_checker](#compression_checker)
* [compressor](#compressor)
* [delay_support_adder](#delay_support_adder)
* [external_binaries](#external_binaries)
* [info_allocator](#info_allocator)
* [placer](#placer)
* [precompressor](#precompressor)
* [router](#router)
* [router_table_compress_as_far_as_possible](#router_table_compress_as_far_as_possible)
* [routing_table_generator](#routing_table_generator)
* [validate_json](#validate_json)
* [validate_routes_uncompressed](#validate_routes_uncompressed)
* [virtual_compressor](#virtual_compressor)
### <a name="compression_checker"></a> compression_checker
#### Trigger
* key: run_compression_checker 
* value: Debug
#### Path
* key: path_compression_checker 
* value: routing_compression_checker_report.rpt
### <a name="compressor"></a> compressor
* key: compressor 
* value: PairOnChipRouterCompression
### <a name="delay_support_adder"></a> delay_support_adder
* key: delay_support_adder 
* value: DelaySupportAdder
### <a name="external_binaries"></a> external_binaries
* key: external_binaries 
* value: None
### <a name="info_allocator"></a> info_allocator
* key: info_allocator 
* value: ZonedRoutingInfoAllocator
### <a name="placer"></a> placer
* key: placer 
* value: ApplicationPlacer
### <a name="precompressor"></a> precompressor
* key: precompressor 
* value: None
### <a name="router"></a> router
* key: router 
* value: ApplicationRouter
### <a name="router_table_compress_as_far_as_possible"></a> router_table_compress_as_far_as_possible
* key: router_table_compress_as_far_as_possible 
* value: False
### <a name="routing_table_generator"></a> routing_table_generator
* key: routing_table_generator 
* value: MergedRoutingTableGenerator
### <a name="validate_json"></a> validate_json
* key: validate_json 
* value: Debug
### <a name="validate_routes_uncompressed"></a> validate_routes_uncompressed
* key: validate_routes_uncompressed 
* value: False
### <a name="virtual_compressor"></a> virtual_compressor
* key: virtual_compressor 
* value: PairCompressor
# <a name="Reports"></a> Reports
* [algorithm_timings](#algorithm_timings)
* [application_graph_placer_report](#application_graph_placer_report)
* [bit_field_compressor_report](#bit_field_compressor_report)
* [board_chip_report](#board_chip_report)
* [clear_iobuf_during_run](#clear_iobuf_during_run)
* [compressed](#compressed)
* [compression_comparison](#compression_comparison)
* [compression_summary](#compression_summary)
* [compressor_iobuf](#compressor_iobuf)
* [data_database](#data_database)
* [data_speed_up_reports](#data_speed_up_reports)
* [dataspec_database](#dataspec_database)
* [default_report_file_path](#default_report_file_path)
* [display_algorithm_timings](#display_algorithm_timings)
* [drift_report](#drift_report)
* [drift_report_ethernet_only](#drift_report_ethernet_only)
* [energy_report](#energy_report)
* [expander_iobuf](#expander_iobuf)
* [extract_iobuf](#extract_iobuf)
* [extract_iobuf_from_binary_types](#extract_iobuf_from_binary_types)
* [extract_iobuf_from_cores](#extract_iobuf_from_cores)
* [fixed_routes_report](#fixed_routes_report)
* [ignores_report](#ignores_report)
* [input_output_database](#input_output_database)
* [java_log](#java_log)
* [json_files](#json_files)
* [json_machine](#json_machine)
* [json_placements](#json_placements)
* [json_routing_tables](#json_routing_tables)
* [max_reports_kept](#max_reports_kept)
* [memory_map_report](#memory_map_report)
* [n_profile_samples](#n_profile_samples)
* [network_graph](#network_graph)
* [network_graph_format](#network_graph_format)
* [network_specification_report](#network_specification_report)
* [partitioner_reports](#partitioner_reports)
* [placement_errors_report](#placement_errors_report)
* [placements](#placements)
* [placements_on_error](#placements_on_error)
* [provenance](#provenance)
* [provenance_report_cutoff](#provenance_report_cutoff)
* [read_graph_provenance_data](#read_graph_provenance_data)
* [read_placements_provenance_data](#read_placements_provenance_data)
* [read_profile_data](#read_profile_data)
* [read_provenance_data_on_end](#read_provenance_data_on_end)
* [read_router_provenance_data](#read_router_provenance_data)
* [redundant_packet_count_report](#redundant_packet_count_report)
* [remove_errored_folders](#remove_errored_folders)
* [router_info_report](#router_info_report)
* [router_reports](#router_reports)
* [router_summary_report](#router_summary_report)
* [sdram_usage_report_per_chip](#sdram_usage_report_per_chip)
* [stack_trace](#stack_trace)
* [tag_allocation_reports](#tag_allocation_reports)
* [text_specs](#text_specs)
* [tpath_algorithm_timings](#tpath_algorithm_timings)
* [tpath_global_provenance](#tpath_global_provenance)
* [tpath_stack_trace](#tpath_stack_trace)
* [uncompressed](#uncompressed)
### <a name="algorithm_timings"></a> algorithm_timings
* key: write_algorithm_timings 
* value: Debug
### <a name="application_graph_placer_report"></a> application_graph_placer_report
#### Trigger
* key: write_application_graph_placer_report 
* value: Info
#### Paths
* key: path_application_graph_placer_report_vertex 
  * value: placement_by_vertex_using_graph.rpt
* key: path_application_graph_placer_report_core 
  * value: placement_by_core_using_graph.rpt
### <a name="bit_field_compressor_report"></a> bit_field_compressor_report
#### Trigger
* key: write_bit_field_compressor_report 
* value: Debug
#### Path
* key: path_bit_field_compressor_report 
* value: bit_field_compressed_summary.rpt
### <a name="board_chip_report"></a> board_chip_report
#### Trigger
* key: write_board_chip_report 
* value: Debug
#### Path
* key: path_board_chip_report 
* value: board_chip_report.txt
### <a name="clear_iobuf_during_run"></a> clear_iobuf_during_run
* key: clear_iobuf_during_run 
* value: True
### <a name="compressed"></a> compressed
#### Trigger
* key: write_compressed 
* value: Debug
#### Path
* key: path_compressed 
* value: compressed_routing_tables_generated
### <a name="compression_comparison"></a> compression_comparison
#### Trigger
* key: write_compression_comparison 
* value: Debug
#### Path
* key: path_compression_comparison 
* value: comparison_of_compressed_uncompressed_routing_tables.rpt
### <a name="compression_summary"></a> compression_summary
#### Trigger
* key: write_compression_summary 
* value: Debug
#### Path
* key: path_compression_summary 
* value: compressed_routing_summary.rpt
### <a name="compressor_iobuf"></a> compressor_iobuf
* key: write_compressor_iobuf 
* value: Debug
### <a name="data_database"></a> data_database
#### Trigger
* key: keep_data_database 
* value: Info
#### Path
* key: path_data_database 
* value: data(reset_str).sqlite3
### <a name="data_speed_up_reports"></a> data_speed_up_reports
#### Trigger
* key: write_data_speed_up_reports 
* value: Debug
#### Paths
* key: path_data_speed_up_reports_speeds 
  * value: speeds_gained_in_speed_up_process.rpt
* key: path_data_speed_up_reports_routers 
  * value: routers_used_in_speed_up_process.rpt
### <a name="dataspec_database"></a> dataspec_database
#### Trigger
* key: keep_dataspec_database 
* value: Debug
#### Path
* key: path_dataspec_database 
* value: ds(reset_str).sqlite3
### <a name="default_report_file_path"></a> default_report_file_path
* key: default_report_file_path 
* value: DEFAULT
### <a name="display_algorithm_timings"></a> display_algorithm_timings
* key: display_algorithm_timings 
* value: True
### <a name="drift_report"></a> drift_report
#### Triggers
* key: write_drift_report_start 
  * value: Debug
* key: write_drift_report_end 
  * value: Debug
#### Path
* key: path_drift_report 
* value: clock_drift.csv
### <a name="drift_report_ethernet_only"></a> drift_report_ethernet_only
* key: drift_report_ethernet_only 
* value: True
### <a name="energy_report"></a> energy_report
#### Trigger
* key: write_energy_report 
* value: False
#### Path
* key: path_energy_report 
* value: energy_report_(n_run).rpt
### <a name="expander_iobuf"></a> expander_iobuf
* key: write_expander_iobuf 
* value: Debug
### <a name="extract_iobuf"></a> extract_iobuf
#### Trigger
* key: extract_iobuf 
* value: Debug
#### Paths
* key: path_iobuf_app 
  * value: provenance_data\app_provenance_data
* key: path_iobuf_system 
  * value: provenance_data\system_provenance_data
### <a name="extract_iobuf_from_binary_types"></a> extract_iobuf_from_binary_types
* key: extract_iobuf_from_binary_types 
* value: None
### <a name="extract_iobuf_from_cores"></a> extract_iobuf_from_cores
* key: extract_iobuf_from_cores 
* value: ALL
### <a name="fixed_routes_report"></a> fixed_routes_report
#### Trigger
* key: write_fixed_routes_report 
* value: Debug
#### Path
* key: path_fixed_routes_report 
* value: fixed_route_routers
### <a name="ignores_report"></a> ignores_report
always written if there is a down core, chip or link declared
#### Path
* key: path_ignores_report 
* value: Ignores_report.rpt
### <a name="input_output_database"></a> input_output_database
#### Trigger
* key: keep_input_output_database 
* value: Info
#### Path
* key: path_input_output_database 
* value: input_output_database.sqlite3
### <a name="java_log"></a> java_log
#### Trigger
* key: keep_java_log 
* value: Debug
#### Path
* key: path_java_log 
* value: jspin.log
### <a name="json_files"></a> json_files
* key: keep_json_files 
* value: Debug
### <a name="json_machine"></a> json_machine
#### Trigger
* key: write_json_machine 
* value: Debug
#### Path
* key: path_json_machine 
* value: json_files\machine.json
### <a name="json_placements"></a> json_placements
#### Trigger
* key: write_json_placements 
* value: Debug
#### Path
* key: path_json_placements 
* value: json_files\placements.json
### <a name="json_routing_tables"></a> json_routing_tables
#### Trigger
* key: write_json_routing_tables 
* value: Debug
#### Path
* key: path_json_routing_tables 
* value: json_files\routing_tables.json
### <a name="max_reports_kept"></a> max_reports_kept
* key: max_reports_kept 
* value: 10
### <a name="memory_map_report"></a> memory_map_report
#### Trigger
* key: write_memory_map_report 
* value: Debug
#### Paths
* key: path_memory_map_report_map 
  * value: memory_map_from_processor_to_address_space
* key: path_memory_map_reports 
  * value: memory_map_reports
### <a name="n_profile_samples"></a> n_profile_samples
* key: n_profile_samples 
* value: 0
### <a name="network_graph"></a> network_graph
#### Trigger
* key: write_network_graph 
* value: Debug
#### Path
* key: path_network_graph 
* value: network_graph.gv
### <a name="network_graph_format"></a> network_graph_format
* key: network_graph_format 
* value: None
### <a name="network_specification_report"></a> network_specification_report
#### Trigger
* key: write_network_specification_report 
* value: Info
#### Path
* key: path_network_specification_report 
* value: network_specification.rpt
### <a name="partitioner_reports"></a> partitioner_reports
#### Trigger
* key: write_partitioner_reports 
* value: Info
#### Path
* key: path_partitioner_reports 
* value: partitioned_by_vertex.rpt
### <a name="placement_errors_report"></a> placement_errors_report
Always run if needed
#### Path
* key: path_placement_errors_report 
* value: placements_error.txt
### <a name="placements"></a> placements
#### Trigger
* key: draw_placements 
* value: False
#### Path
* key: path_placements 
* value: placements.png
### <a name="placements_on_error"></a> placements_on_error
#### Trigger
* key: draw_placements_on_error 
* value: False
#### Path
* key: path_placements_on_error 
* value: placements_error.png
### <a name="provenance"></a> provenance
* key: write_provenance 
* value: Info
### <a name="provenance_report_cutoff"></a> provenance_report_cutoff
* key: provenance_report_cutoff 
* value: 20
### <a name="read_graph_provenance_data"></a> read_graph_provenance_data
* key: read_graph_provenance_data 
* value: Debug
### <a name="read_placements_provenance_data"></a> read_placements_provenance_data
* key: read_placements_provenance_data 
* value: Debug
### <a name="read_profile_data"></a> read_profile_data
* key: read_profile_data 
* value: Debug
### <a name="read_provenance_data_on_end"></a> read_provenance_data_on_end
* key: read_provenance_data_on_end 
* value: Debug
### <a name="read_router_provenance_data"></a> read_router_provenance_data
* key: read_router_provenance_data 
* value: Debug
### <a name="redundant_packet_count_report"></a> redundant_packet_count_report
#### Trigger
* key: write_redundant_packet_count_report 
* value: Info
#### Path
* key: path_redundant_packet_count_report 
* value: redundant_packet_count.rpt
### <a name="remove_errored_folders"></a> remove_errored_folders
* key: remove_errored_folders 
* value: True
### <a name="router_info_report"></a> router_info_report
#### Trigger
* key: write_router_info_report 
* value: Info
#### Path
* key: path_router_info_report 
* value: virtual_key_space_information_report.rpt
### <a name="router_reports"></a> router_reports
#### Trigger
* key: write_router_reports 
* value: Debug
#### Path
* key: path_router_reports 
* value: edge_routing_info.rpt
### <a name="router_summary_report"></a> router_summary_report
#### Trigger
* key: write_router_summary_report 
* value: Debug
#### Path
* key: path_router_summary_report 
* value: routing_summary.rpt
### <a name="sdram_usage_report_per_chip"></a> sdram_usage_report_per_chip
#### Trigger
* key: write_sdram_usage_report_per_chip 
* value: Info
#### Path
* key: path_sdram_usage_report_per_chip 
* value: chip_sdram_usage_by_core.rpt
### <a name="stack_trace"></a> stack_trace
* key: keep_stack_trace 
* value: Info
### <a name="tag_allocation_reports"></a> tag_allocation_reports
#### Trigger
* key: write_tag_allocation_reports 
* value: Debug
#### Paths
* key: path_tag_allocation_reports_host 
  * value: tags.rpt
* key: path_tag_allocation_reports_machine 
  * value: tags_on_machine.txt
### <a name="text_specs"></a> text_specs
#### Trigger
* key: write_text_specs 
* value: Debug
#### Path
* key: path_text_specs 
* value: data_spec_text_files
### <a name="tpath_algorithm_timings"></a> tpath_algorithm_timings
* key: tpath_algorithm_timings 
* value: algorithm_timings.rpt
### <a name="tpath_global_provenance"></a> tpath_global_provenance
* key: tpath_global_provenance 
* value: global_provenance.sqlite3
### <a name="tpath_stack_trace"></a> tpath_stack_trace
* key: tpath_stack_trace 
* value: stack_trace
### <a name="uncompressed"></a> uncompressed
#### Trigger
* key: write_uncompressed 
* value: Debug
#### Path
* key: path_uncompressed 
* value: routing_tables_generated
# <a name="Buffers"></a> Buffers
* [minimum_auto_time_steps](#minimum_auto_time_steps)
* [use_auto_pause_and_resume](#use_auto_pause_and_resume)
### <a name="minimum_auto_time_steps"></a> minimum_auto_time_steps
* key: minimum_auto_time_steps 
* value: 1000
### <a name="use_auto_pause_and_resume"></a> use_auto_pause_and_resume
* key: use_auto_pause_and_resume 
* value: True
# <a name="Mode"></a> Mode
* [mode](#mode)
* [violate_1ms_wall_clock_restriction](#violate_1ms_wall_clock_restriction)
### <a name="mode"></a> mode
* key: mode 
* value: Production
### <a name="violate_1ms_wall_clock_restriction"></a> violate_1ms_wall_clock_restriction
* key: violate_1ms_wall_clock_restriction 
* value: False
# <a name="EnergyMonitor"></a> EnergyMonitor
* [n_samples_per_recording_entry](#n_samples_per_recording_entry)
* [sampling_frequency](#sampling_frequency)
### <a name="n_samples_per_recording_entry"></a> n_samples_per_recording_entry
* key: n_samples_per_recording_entry 
* value: 100
### <a name="sampling_frequency"></a> sampling_frequency
* key: sampling_frequency 
* value: 10
# <a name="Java"></a> Java
* [java_call](#java_call)
* [java_jar_path](#java_jar_path)
* [java_properties](#java_properties)
* [java_spinnaker_path](#java_spinnaker_path)
* [use_java](#use_java)
### <a name="java_call"></a> java_call
* key: java_call 
* value: java
### <a name="java_jar_path"></a> java_jar_path
* key: java_jar_path 
* value: None
### <a name="java_properties"></a> java_properties
* key: java_properties 
* value: None
### <a name="java_spinnaker_path"></a> java_spinnaker_path
* key: java_spinnaker_path 
* value: None
### <a name="use_java"></a> use_java
#### Trigger
* key: use_java 
* value: False
#### Path
* key: path_json_java_placements 
* value: json_files\java_placements.json
# <a name="Simulation"></a> Simulation
* [drop_late_spikes](#drop_late_spikes)
* [error_on_non_spynnaker_pynn](#error_on_non_spynnaker_pynn)
* [incoming_spike_buffer_size](#incoming_spike_buffer_size)
* [n_colour_bits](#n_colour_bits)
* [ring_buffer_sigma](#ring_buffer_sigma)
* [spikes_per_second](#spikes_per_second)
* [transfer_overhead_clocks](#transfer_overhead_clocks)
### <a name="drop_late_spikes"></a> drop_late_spikes
* key: drop_late_spikes 
* value: False
### <a name="error_on_non_spynnaker_pynn"></a> error_on_non_spynnaker_pynn
* key: error_on_non_spynnaker_pynn 
* value: True
### <a name="incoming_spike_buffer_size"></a> incoming_spike_buffer_size
* key: incoming_spike_buffer_size 
* value: 256
### <a name="n_colour_bits"></a> n_colour_bits
* key: n_colour_bits 
* value: 4
### <a name="ring_buffer_sigma"></a> ring_buffer_sigma
* key: ring_buffer_sigma 
* value: 5
### <a name="spikes_per_second"></a> spikes_per_second
* key: spikes_per_second 
* value: 30
### <a name="transfer_overhead_clocks"></a> transfer_overhead_clocks
* key: transfer_overhead_clocks 
* value: 200
# <a name="Recording"></a> Recording
* [live_spike_host](#live_spike_host)
* [live_spike_port](#live_spike_port)
### <a name="live_spike_host"></a> live_spike_host
* key: live_spike_host 
* value: 0.0.0.0
### <a name="live_spike_port"></a> live_spike_port
* key: live_spike_port 
* value: 17895
# <a name="report_files"></a> Report Files
  * [Ignores_report.rpt](#ignores_report)
  * [bit_field_compressed_summary.rpt](#bit_field_compressor_report)
  * [board_chip_report.txt](#board_chip_report)
  * [chip_sdram_usage_by_core.rpt](#sdram_usage_report_per_chip)
  * [clock_drift.csv](#drift_report)
  * [comparison_of_compressed_uncompressed_routing_tables.rpt](#compression_comparison)
  * [compressed_routing_summary.rpt](#compression_summary)
  * [compressed_routing_tables_generated](#compressed)
  * [data(reset_str).sqlite3](#data_database)
  * [data_spec_text_files](#text_specs)
  * [ds(reset_str).sqlite3](#dataspec_database)
  * [edge_routing_info.rpt](#router_reports)
  * [energy_report_(n_run).rpt](#energy_report)
  * [fixed_route_routers](#fixed_routes_report)
  * [input_output_database.sqlite3](#input_output_database)
  * [json_files\java_placements.json](#use_java)
  * [json_files\machine.json](#json_machine)
  * [json_files\placements.json](#json_placements)
  * [json_files\routing_tables.json](#json_routing_tables)
  * [jspin.log](#java_log)
  * [memory_map_from_processor_to_address_space](#memory_map_report)
  * [memory_map_reports](#memory_map_report)
  * [network_graph.gv](#network_graph)
  * [network_specification.rpt](#network_specification_report)
  * [partitioned_by_vertex.rpt](#partitioner_reports)
  * [placement_by_core_using_graph.rpt](#application_graph_placer_report)
  * [placement_by_vertex_using_graph.rpt](#application_graph_placer_report)
  * [placements.png](#placements)
  * [placements_error.png](#placements_on_error)
  * [placements_error.txt](#placement_errors_report)
  * [provenance_data\app_provenance_data](#extract_iobuf)
  * [provenance_data\system_provenance_data](#extract_iobuf)
  * [redundant_packet_count.rpt](#redundant_packet_count_report)
  * [routers_used_in_speed_up_process.rpt](#data_speed_up_reports)
  * [routing_compression_checker_report.rpt](#compression_checker)
  * [routing_summary.rpt](#router_summary_report)
  * [routing_tables_generated](#uncompressed)
  * [speeds_gained_in_speed_up_process.rpt](#data_speed_up_reports)
  * [tags.rpt](#tag_allocation_reports)
  * [tags_on_machine.txt](#tag_allocation_reports)
  * [virtual_key_space_information_report.rpt](#router_info_report)
