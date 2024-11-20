
# Instructions for using DYNAMIC_INPUT_TARGETS

By default, the commands for `make correctness` and `make benchmark` will run on all inputs in the inputs/ directory. You can target specific benchmarks by using the DYNAMIC_INPUT_TARGETS environment variable.

For example, you can run the following command: 

```bash
DYNAMIC_INPUT_TARGETS=random_10k_50k.json,random_1k_5k.json make correctness
```

The above precise format is used by the server, but there is a little bit of flexibility. For example, the following should all work and be equivalent:

```bash
DYNAMIC_INPUT_TARGETS="random_10k_50k,random_1k_5k" make correctness
DYNAMIC_INPUT_TARGETS="random_10k_50k.json,random_1k_5k.json" make correctness
DYNAMIC_INPUT_TARGETS="random_10k_50k.json,random_1k_5k.json" make correctness
DYNAMIC_INPUT_TARGETS="./inputs/random_10k_50k.json,./inputs/random_1k_5k.json" make correctness
DYNAMIC_INPUT_TARGETS="./inputs/random_10k_50k,./inputs/random_1k_5k" make correctness
```

# Submitting the problem to Speedcode

## Step 1: go to speedcode.org/contribute 

When you first go to this url, you may be redirected back to speedcode.org/ide/index.html. This is a common occurrence. If this happens, just go back to speedcode.org/contribute and it should not happen again for another 30-60 minutes.

## Step 2: Copy API key

On speedcode.org/contribute you should copy your API key.

## Step 3: Run 'make submit'

Run the command `make submit` from the problem directory. When prompted, paste your API key.

## Step 4: View problem on speedcode

The output of `make submit` should include the following, if it is successful:

```bash
<Response [204]>
###################################################################################
###################################################################################
URL: https://speedcode.org/ide/contest.html?d239d386-64e9-4404-aab5-68e18e1c310e
###################################################################################
###################################################################################
```

You can go to the specified URL to try out the problem on speedcode.


## Step 5: Test the problem.

Test the problem on speedcode.org. Note that, the reference results and driver objects will not be cached for the first execution for a new problem. So your first runs may be slow. You can populate the cache for all problems by selecting all graphs in the UI and then clicking submit. The server uses a separate timeout per-execution when generating cached results for the reference implementation, so this should not result in a timeout.

## Step 6: Associate the problem with the constant ID for the PPoPP competition.

**Explanation later**.

# Preparing problem for submission.

There are two important files for each speedcode problem that are generated automatically using the command:

```bash
python -m input_schema.make_manifest 
usage: make_manifest.py [-h] [--input_targets INPUT_TARGETS [INPUT_TARGETS ...]] --default_run_targets DEFAULT_RUN_TARGETS [DEFAULT_RUN_TARGETS ...] --default_cilksan_target DEFAULT_CILKSAN_TARGET --default_cilkscale_target DEFAULT_CILKSCALE_TARGET [--allowed_run_targets [ALLOWED_RUN_TARGETS ...]]
                        [--submit_targets [SUBMIT_TARGETS ...]] [--allowed_cilksan_targets [ALLOWED_CILKSAN_TARGETS ...]]
```

This creates two files: `./inputs/INPUT_MANIFEST` and `./data/data_manifest.json`. *It is preferred that you do not manually edit these files as the schema for the manifests is relied upon by the various components of Speedcode.*

**Note/TODO**: We will need to modify the `INPUT_MANIFEST` schema to include short descriptions for the inputs.

The `INPUT_MANIFEST` contains information about the valid input targets for speedcode problems. The `INPUT_MANIFEST` is used by the frontend to display the available inputs when setting "run options".

The `data_manifest.json` file contains information that maps binary names that appear in `inputs/*.json` files to resources on S3. If you are running locally and there is a file `data/graph_data.bin` the data manifest will map this file to `ppopp-graphs/graph_data.bin`. When the code is executed on worker machines, the data maniest is used to identify input files that depend on external files, and then fetch those external files and place them in the `data/` directory.

The `input_schema.make_manifest` script will identify inputs that depend on external resources, and automatically populate the `data_manifest.json` file correctly.


