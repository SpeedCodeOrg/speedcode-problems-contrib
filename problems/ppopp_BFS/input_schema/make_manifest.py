import argparse
from typing import List, Union, Optional
from pydantic import BaseModel
from pathlib import Path
import json
import sys
import random
import numpy as np
from input_schema.schema import Input
import os
from models.problem_response_models import PRM_DataManifest, PRM_DataManifestItem, PRM_InputManifest

if __name__ == "__main__":
   
   files = os.listdir("inputs")
   filtered_files = []
   manifest_items = []
   for f in files:
      if f.endswith(".json"):
         filtered_files.append(f)
   all_input_targets = filtered_files[:]
   parser = argparse.ArgumentParser()

   parser.add_argument("--input_targets", type=str, nargs='+', default=all_input_targets)
   parser.add_argument("--default_run_targets", type=str, nargs='+', required=True)
   parser.add_argument("--default_cilksan_target", type=str, required=True)
   parser.add_argument("--default_cilkscale_target", type=str, required=True)
   parser.add_argument("--allowed_run_targets", type=str, nargs='*', default=None)
   parser.add_argument("--submit_targets", type=str, nargs='*', default=None)
   parser.add_argument("--allowed_cilksan_targets", type=str, nargs='*', default=None)
   args = parser.parse_args()
   print(args)

   # validate the input manifest.
   input_targets = []
   for x in args.input_targets:
      target_name = Path(x).stem
      assert Path(f'inputs/{target_name}.json').exists()
      input_targets.append(target_name)

   default_run_targets = []
   for x in args.default_run_targets:
      target_name = Path(x).stem
      assert target_name in input_targets
      default_run_targets.append(target_name)
   
   default_cilksan_target = Path(args.default_cilksan_target).stem
   default_cilkscale_target = Path(args.default_cilkscale_target).stem

   assert default_cilksan_target in input_targets
   assert default_cilkscale_target in input_targets

   if args.allowed_run_targets == None:
      allowed_run_targets = input_targets
   if args.submit_targets == None:
      submit_targets = input_targets
   if args.allowed_cilksan_targets == None:
      allowed_cilksan_targets = allowed_run_targets
   allowed_cilkscale_targets = allowed_run_targets 

   input_manifest = PRM_InputManifest(\
      input_targets = input_targets,\
      default_run_targets=default_run_targets,\
      allowed_run_targets=allowed_run_targets,\
      submit_targets=submit_targets,\
      allowed_cilksan_targets=allowed_cilksan_targets,\
      default_cilksan_target = default_cilksan_target,\
      default_cilkscale_target = default_cilkscale_target,\
      allowed_cilkscale_targets = allowed_cilkscale_targets)
   print(input_manifest)
   open('inputs/INPUT_MANIFEST','w+').write(input_manifest.json())

   for f in filtered_files:
      input = Input.parse_raw(open('inputs/'+f).read())
      #print(input)
      if hasattr(input.graph, 'data_file_format') and input.graph.data_file_format:
        manifest_items.append(\
           PRM_DataManifestItem(input_target=f, data_directory="ppopp-graphs-v2", data_files=[input.graph.filename]))
        
   manifest=PRM_DataManifest(quickrun_targets=[], submission_targets=[], manifest_items=manifest_items)
   open('data/data_manifest.json', 'w+').write(manifest.json())

   quit()

   if args.save_to_binary:
       assert(args.save_filename != None)

   if args.format == 'data_file_format':
       assert(args.filename != None)

   if args.format == 'coo_format' or args.format == 'random_generated_graph':
       assert(args.num_vertices != 0 and args.num_edges_per_vertex != 0)
       
   meta_info = None
   if args.save_to_binary:
       meta_info = MetaInfo(save_to_binary=args.save_to_binary, save_filename=args.save_filename)

   if args.format == 'data_file_format':
       open(args.output_file,'w+').write(Input(graph=DataFileFormat(filename=args.filename, file_format=args.file_format), meta_info=meta_info).json())
       quit()
   if args.format == 'coo_format':
       open(args.output_file,'w+').write(coo_format_gen(args.num_vertices, args.num_edges_per_vertex, meta_info=meta_info).json())
       quit()
   if args.format == 'random_generated_graph':
       open(args.output_file, 'w+')(Input(graph=RandomGeneratedGraph(num_vertices=args.num_vertices, num_edges_per_vertex=args.num_edges_per_vertex), meta_info=meta_info).json())
       quit() 

   #print(args)
   #quit()
   #N = int(sys.argv[1])
   #print(main(N))

         

