---
title: Example Mapping Files

# The version described here is no longer supported. 

[Home page for current version](/) 

files:
  - name: machine.json
    info: The machine in use
  - name: partitioned_graph.json
    info: The graph representation of the problem, after partitioning
  - name: constraints.json
    info: The constraints on the machine, resources, vertices, or edges
  - name: placements.json
    info: The placements of the vertices of the graph
  - name: routing_paths.json
    info: The routing of the edges through the chips
  - name: core_allocations.json
    info: The allocations of cores to vertices
  - name: sdram_allocations.json
    info: The allocation of SDRAM to vertices
---

<dl>
{% for file in page.files %}
    <dt><a href="http://spinnaker.cs.man.ac.uk/docs/mapping_example_files/{{file.name}}">{{file.name}}</a></dt>
    <dd>{{file.info}}</dd>
{% endfor %}
</dl>
