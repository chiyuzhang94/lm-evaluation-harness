# TODO: Remove all TODO comments once the implementation is complete.
"""
TODO: Add the Paper Title on this line.
TODO: Add the paper's PDF URL (preferably from arXiv) on this line.

TODO: Write a Short Description of the task.

Homepage: TODO: Add the URL to the task's Homepage here.
"""
from lm_eval.base import Task
import transformers.data.metrics.squad_metrics as squad_metrics
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, classification_report, confusion_matrix
from lm_eval.base import rf,mean
import lm_eval.metrics as me
import numpy as np
import json
import os
# TODO: Add the BibTeX citation for the task.
_CITATION = """
"""


# TODO: Replace `NewTask` with the name of your Task.
class IronySarcasm(Task):
    VERSION = 0
    # TODO: Add the `DATASET_PATH` string. This will be the name of the `Task`
    # dataset as denoted in HuggingFace `datasets`.
    DATASET_PATH = None
    # TODO: Add the `DATASET_NAME` string. This is the name of a subset within
    # `DATASET_PATH`. If there aren't specific subsets you need, leave this as `None`.
    DATASET_NAME = None

    def __init__(self):
        # Load the metadata

        self._training_docs = None
        self._fewshot_docs = None
        # super().__init__(data_dir, cache_dir, download_mode)
        # self.DATASET_NAME = task_name
        # self.dataset = self.download()

    def set_dataset_info(self, data_path, task_name):
        self.DATASET_NAME = task_name
        self.DATASET_PATH = data_path
        with open(f"{self.DATASET_PATH}/data/{task_name}/label2ind.json") as json_file:
            self.label2ind = json.load(json_file)

    def set_model_name(self, model_name):
        self.model_name = model_name

    def has_training_docs(self):
        # TODO: Fill in the return with `True` if the Task has training data; else `False`.
        return False

    def has_validation_docs(self):
        # TODO: Fill in the return with `True` if the Task has validation data; else `False`.
        return False

    def has_test_docs(self):
        # TODO: Fill in the return with `True` if the Task has test data; else `False`.
        return True

    def training_docs(self):
        if self.has_training_docs():
            # We cache training documents in `self._training_docs` for faster
            # few-shot processing. If the data is too large to fit in memory,
            # return the training data as a generator instead of a list.
            if self._training_docs is None:
                # TODO: Return the training document generator from `self.dataset`.
                # If you need to process the data, `map` over the documents with
                # the custom processing function, `self._process_doc`. E.g.
                # `map(self._process_doc, self.dataset["validation"])`
                # In most case you can leave this as is unless the dataset split is
                # named differently than the default `"train"`.
                self._training_docs = list(self.dataset["train"])
            return self._training_docs

    def validation_docs(self):
        if self.has_validation_docs():
            # TODO: Return the validation document generator from `self.dataset`.
            # If you need to process the data, `map` over the documents with the
            # custom processing function, `self._process_doc`. E.g.
            # `map(self._process_doc, self.dataset["validation"])`
            # In most case you can leave this as is unless the dataset split is
            # named differently than the default `"validation"`.
            return self.dataset["validation"]

    def test_docs(self):
        if self.has_test_docs():
            # TODO: Return the test document generator from `self.dataset`.
            # If you need to process the data, `map` over the documents with the
            # custom processing function, `self._process_doc`. E.g.
            # `map(self._process_doc, self.dataset["test"])`
            # In most case you can leave this as is unless the dataset split is
            # named differently than the default `"test"`.
            self.gold_list=[]
            self.pred_list=[]
            return self.dataset["test"]

    def _process_doc(self, doc):
        # TODO: Process (detokenize, strip, replace etc.) each individual `doc`
        # with this function. You can map this across the docs in each available
        # dataset split. See the TODOs in `train_docs`, `validation_docs`, and
        # `test_docs` for snippets.
        # NOTE: DELETE THIS FUNCTION IF UNUSED.
        return doc

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.

        label_prompt=""
        keys=list(self.label2ind.keys())
        if "Others" in keys:
            keys.remove("Others")
            keys.append("Others")
        if "Not" in keys:
            keys.remove("Not")
            keys.append("Not")
            
        label_prompt = ", ".join(keys[:-1])
        label_prompt += f", or {keys[-1]}"
        label_prompt = label_prompt.lower()
        label_prompt = label_prompt.replace('_', ' ')

        if self.DATASET_NAME in ["irony-type-2018-hee-eng"]:
            text = doc["content"]+f"\nQuestion: Is the type of this text {label_prompt}?\nAnswer:"
        else:
            text = doc["content"]+f"\nQuestion: Is this sentence {label_prompt}?\nAnswer:"
            
        if self.prompt_wrapper:
            text = self.prompt_wrapper.format(text)
            
        assert text is not None

        return text
    
    
    
    
    
    
    def doc_to_target(self, doc):
        # TODO: Fill in the `target` ("gold answer") variable.
        # The prepended `" "` is required to space out the `doc_to_text` and
        # `doc_to_target` strings.
        target = doc["label"].replace('_', ' ')
        return " " + target

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or
            test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        ll_list=[]
        for key in self.label2ind.keys():
            res, _ = rf.loglikelihood(ctx, key)
            ll_list.append(res)
        #ll_Anger, _ = rf.loglikelihood(ctx, " Anger")
        #ll_Joy, _ = rf.loglikelihood(ctx, " Joy")
        #ll_Optimism, _ = rf.loglikelihood(ctx, " Optimism")
        #ll_Sadness, _ = rf.loglikelihood(ctx, " Sadness")
        return ll_list

    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a
        dict where keys are the names of submetrics and values are the values of
        the metric for that one document

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        #text2digit={"Anger": 0, "Joy": 1, "Optimism": 2, "Sadness": 3}
        ind2label = dict((v,k) for k,v in self.label2ind.items())
        gold = doc["label"]
        pred = np.argmax(results)
        
        pred=ind2label[pred]
        #scores = self.compute_scores(gold, pred)
        self.gold_list.append(gold)
        self.pred_list.append(pred)
        return {"f1": 0}

    def aggregation(self):
        """
        :returns: {str: [metric_score] -> float}
            A dictionary where keys are the names of submetrics and values are
            functions that aggregate a list of metric scores
        """
        # TODO: For each (sub)metric in the task evaluation, add a key-value pair
        # with the metric name as key and an aggregation function as value which
        # determines how to combine results from each document in the dataset.
        # Check `lm_eval.metrics` to find built-in aggregation functions.
        
        accuracy = accuracy_score(self.gold_list, self.pred_list)
        f1score_ma = f1_score(self.gold_list, self.pred_list, average='macro') 
        f1score_mi = f1_score(self.gold_list, self.pred_list, average='micro') 
        f1score_wei = f1_score(self.gold_list, self.pred_list, average='weighted') 

        recall = recall_score(self.gold_list, self.pred_list, average='macro')
        precision = precision_score(self.gold_list, self.pred_list, average='macro')
        report = classification_report(self.gold_list, self.pred_list, digits=6)
        
        results = {
            'accuracy': accuracy,
            'f1score_ma':f1score_ma,
            'f1score_mi':f1score_mi,
            'f1score_wei':f1score_wei,
            'recall':recall,
            'precision':precision,
            'report':report
        }
        
        model_dir = f"{os.getcwd()}/results/{self.model_name}"
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

        with open(f"{model_dir}/{self.DATASET_NAME}.json", "w") as f:
            json.dump(results, f)

        with open(f"{model_dir}/{self.DATASET_NAME}_gold.txt", 'w') as f:
            for line in self.gold_list:
                f.write(f"{line}\n")
        with open(f"{model_dir}/{self.DATASET_NAME}_pred.txt", 'w') as f:
            for line in self.pred_list:
                f.write(f"{line}\n")
        return {"f1": mean}

    def higher_is_better(self):
        # TODO: For each (sub)metric in the task evaluation, add a key-value pair
        # with the metric name as key and a `bool` value determining whether or
        # not higher values of that metric are deemed better.
        return {"f1": True}