import argparse
import json
import logging
import fnmatch

from lm_eval import tasks, evaluator

logging.getLogger("openai").setLevel(logging.WARNING)


class MultiChoice:
    def __init__(self, choices):
        self.choices = choices

    # Simple wildcard support (linux filename patterns)
    def __contains__(self, values):
        for value in values.split(","):
            if len(fnmatch.filter(self.choices, value)) == 0:
                return False

        return True

    def __iter__(self):
        for choice in self.choices:
            yield choice


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--model_args", required=True, default="")
    parser.add_argument("--tasks", required=True, default=None, choices=MultiChoice(tasks.ALL_TASKS))
    parser.add_argument("--task_list", required=True, default=None)
    parser.add_argument("--model_name", required=True, default=None)
    parser.add_argument("--data_path", required=True)
    parser.add_argument("--prompt_wrapper", default=None)
    parser.add_argument("--provide_description", action="store_true")
    parser.add_argument("--num_fewshot", type=int, default=0)
    parser.add_argument("--batch_size", type=str, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--output_path", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no_cache", action="store_true")
    parser.add_argument("--decontamination_ngrams_path", default=None)
    parser.add_argument("--description_dict_path", default=None)
    parser.add_argument("--check_integrity", action="store_true")
    

    return parser.parse_args()


# Returns a list containing all values of the source_list that
# match at least one of the patterns
def pattern_match(patterns, source_list):
    task_names = set()
    for pattern in patterns:
        for matching in fnmatch.filter(source_list, pattern):
            task_names.add(matching)
    return sorted(list(task_names))


def main():
    args = parse_args()

    assert not args.provide_description  # not implemented

    if args.limit:
        print(
            "WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
        )

    if args.tasks is None:
        task_names = tasks.ALL_TASKS
    else:
        task_names = pattern_match(args.tasks.split(","), tasks.ALL_TASKS)

    print(f"Selected Tasks: {task_names}")

    description_dict = {}
    if args.description_dict_path:
        with open(args.description_dict_path, "r") as f:
            description_dict = json.load(f)

    task_list = args.task_list.split(',')   # the format of args.task_list: "task_1,task_2,task3,..."
    if args.prompt_wrapper is not None:
        prompt_wrapper = open(args.prompt_wrapper, "r").read()
    else:
        prompt_wrapper = None
    list_of_results = evaluator.simple_evaluate(
        prompt_wrapper=prompt_wrapper,
        data_path=args.data_path,
        model_name=args.model_name,
        task_list=task_list,
        model=args.model,
        model_args=args.model_args,
        tasks=task_names,
        num_fewshot=args.num_fewshot,
        batch_size=args.batch_size,
        device=args.device,
        no_cache=args.no_cache,
        limit=args.limit,
        description_dict=description_dict,
        decontamination_ngrams_path=args.decontamination_ngrams_path,
        check_integrity=args.check_integrity,
    )

    for results in list_of_results:
        dumped = json.dumps(results, indent=2)
        print(dumped)

        if args.output_path:
            with open(args.output_path, "w") as f:
                f.write(dumped)

        print(
            f"{args.model} ({args.model_args}), limit: {args.limit}, provide_description: {args.provide_description}, "
            f"num_fewshot: {args.num_fewshot}, batch_size: {args.batch_size}"
        )
        print(evaluator.make_table(results))


if __name__ == "__main__":
    main()
