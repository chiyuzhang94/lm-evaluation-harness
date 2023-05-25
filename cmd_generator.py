import argparse


task_dict = {
    "other_task": [
       "aggressive-2018-kumar-hin",
        "dangerous-2020-alshehri-ara",
        "hate-2016-waseem-eng",
        "hate-2017-davidson-eng",
        "hate-2018-alakrot-ara",
        "hate-2018-bosco-ita",
        "hate-2019-cabasag-fil",
        "hate-2019-mulki-ara",
        "hate-2019-basile-eng",
        "hate-2019-basile-spa",
        "hate-2019-fortuna-por",
        "hate-2019-ptaszynski-pol",
        "hate-2020-moon-kor",
        "hate-2020-mubarak-ara",
        "hate-2022-deng-zho",
        "hate-2022-jeong-kor",
        "hate-2022-marreddy-tel",
        "sexism-2020-chiril-fre",
        "offensive-2019-zampieri-eng",
        "offensive-2020-zampieri-ara",
        "offensive-2020-zampieri-dan",
        "offensive-2020-zampieri-ell",
        "offensive-2020-zampieri-tur",
        "offensive-2020-mubarak-ara",
        "offensive-2021-novak-slv",
        "offensive-group-2019-zampieri-eng",
        "hate-group-2019-ousidhoum-ara",
        "hate-group-2019-ousidhoum-fre",
        "offensive-target-2019-zampieri-eng",
        "hate-target-2019-ousidhoum-ara",
        "hate-target-2019-ousidhoum-fre",
        "hate-target-2020-karim-ben",
        "offense-target-2022-chakravarthi-kan",
        "offense-target-2022-chakravarthi-mal",
        "offense-target-2022-chakravarthi-tam",
        "hate-target-2022-jeong-kor"
    ],
    "irony_sarcasm_task": [
        "irony-2014-basile-ita",
        "irony-2016-barbieri-spa",
        "irony-2018-hee-eng",
        "irony-2018-cignarella-ita",
        "irony-2018-vijay-hin",
        "irony-2019-ghanem-ara",
        "irony-2019-ortega-spa",
        "irony-2020-golazizian-fas",
        "irony-2020-xiang-zho",
        "sarcasm-2012-walker-eng",
        "sarcasm-2013-riloff-eng",
        "sarcasm-2014-ptacek-ces",
        "sarcasm-2014-ptacek-eng",
        "sarcasm-2015-bamman-eng",
        "sarcasm-2015-rajadesingan-eng",
        "sarcasm-2016-oraby-eng",
        "sarcasm-2020-gong-zho",
        "sarcasm-2020-abufarha-ara",
        "sarcasm-2021-farha-ara",
        "irony-type-2018-hee-eng",
    ],
    "subjective_task": [
        "subjevtive-2004-pang-eng",
        "subjective-2013-jang-kor",
        "subject-2014-basile-ita",
        "subject-2016-basile-ita",
        "subjective-2016-barbieri-spa",
        "subjective-2022-priban-ces",
    ],
    "humor_task": [
        "humor-2020-aggarwal-hin",
        "humor-2019-blinov-rus",
        "humor-2021-chiruzzo-spa",
        "humor-2021-meaney-eng",
    ],
    "emotion_task": [
        'emotion-1986-wallbott-eng',
        'emotion-2015-lee-zho',
        'emotion-2018-kajava-fin',
        'emotion-2018-kajava-fre',
        'emotion-2018-kajava-ita',
        'emotion-2018-husein-msa',
        'emotion-2020-abdul-ara',
        'emotion-2018-mohammad-eng',
        'emotion-2018-mohammad-ara',
        'emotion-2018-mohammad-spa',
        'emotion-2019-saputri-ind',
        'emotion-2020-guven-tur',
        'emotion-2020-wilie-ind',
        'emotion-2019-ho-vie',
        'emotion-2020-plaza-eng',
        'emotion-2020-plaza-spa',
        'emotion-2020-ohman-fin',
        'emotion-2020-demszky-eng',
        'emotion-2021-bianchi-ita',
        'emotion-2021-ciobotaru-ron',
        'emotion-2021-debaditya-hin',
        'emotion-2021-cortiz-por',
        'emotion-2021-sabri-fas',
        'emotion-2021-sboev-rus',
        'emotion-2022-iqbal-ben',
        'emotion-2022-bianchi-fre',
        'emotion-2022-bianchi-deu',
    ],
    "sentiment_task": [
        'sentiment-2005-pang-eng',
        'sentiment-2008-tan-zho',
        'sentiment-tw-2012-thelwall-eng',
        'sentiment-yt-2012-thelwall-eng',
        'sentiment-5-2013-socher-eng',
        'sentiment-2013-jang-kor',
        'sentiment-2013-socher-eng',
        'sentiment-2014-basile-ita',
        'sentiment-2016-basile-ita',
        'sentiment-2016-dingli-mlt',
        'sentiment-2016-mozetic-bul',
        'sentiment-2016-mozetic-bos',
        'sentiment-2016-mozetic-deu',
        'sentiment-2016-mozetic-eng',
        'sentiment-2016-mozetic-spa',
        'sentiment-2016-mozetic-hrv',
        'sentiment-2016-mozetic-hun',
        'sentiment-2016-mozetic-pol',
        'sentiment-2016-mozetic-por',
        'sentiment-2016-mozetic-rus',
        'sentiment-2016-mozetic-slk',
        'sentiment-2016-mozetic-slv',
        'sentiment-2016-mozetic-sqi',
        'sentiment-2016-mozetic-srp',
        'sentiment-2016-mozetic-swe',
        'sentiment-2016-rei-deu',
        'sentiment-2016-rei-spa',
        'sentiment-2016-rei-ita',
        'sentiment-2017-rosenthal-eng',
        'sentiment-2018-patra-ben',
        'sentiment-2018-patra-hin',
        'sentiment-2018-amram-heb',
        'sentiment-2018-brum-por',
        'sentiment-2018-kajava-fin',
        'sentiment-2018-kajava-fre',
        'sentiment-2018-kajava-ita',
        'sentiment-2018-velldal-nor',
        'sentiment-2019-kocon-pol',
        'sentiment-2019-suriyawongkul-tha',
        'sentiment-2020-wan-zho',
        'sentiment-2020-ashrafi-fas',
        'sentiment-2020-dumitrescu-ron',
        'sentiment-2020-oyewusi-pcm',
        'sentiment-2020-rybak-pol',
        'sentiment-2020-wilie-ind',
        'sentiment-2021-abdul-ara',
        'sentiment-2021-diallo-bam',
        'sentiment-2021-islam-ben',
        'sentiment-2021-kulkarni-mar',
        'sentiment-2022-chakravarthi-kan',
        'sentiment-2022-chakravarthi-mal',
        'sentiment-2022-chakravarthi-tam',
        'sentiment-2022-muhammad-ara',
        'sentiment-2022-muhammad-amh',
        'sentiment-2022-muhammad-ary',
        'sentiment-2022-muhammad-arq',
        'sentiment-2022-muhammad-hau',
        'sentiment-2022-muhammad-ibo',
        'sentiment-2022-muhammad-pcm',
        'sentiment-2022-muhammad-kin',
        'sentiment-2022-muhammad-swh',
        'sentiment-2022-muhammad-tso',
        'sentiment-2022-muhammad-twi',
        'sentiment-2022-muhammad-yor',
        'sentiment-2022-shode-yor',
        'sentiment-2022-suzuki-jpn',
        'sentiment-2022-winata-ace',
        'sentiment-2022-winata-ban',
        'sentiment-2022-winata-bbc',
        'sentiment-2022-winata-bjn',
        'sentiment-2022-winata-bug',
        'sentiment-2022-winata-jav',
        'sentiment-2022-winata-mad',
        'sentiment-2022-winata-min',
        'sentiment-2022-winata-nij',
        'sentiment-2022-winata-sun',
        'sentiment-2022-marreddy-tel',
    ],
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--model_args", required=True)
    parser.add_argument("--model_name", required=True)
    parser.add_argument("--data_path", required=True)
    parser.add_argument("--prompt_wrapper", default=None)
    parser.add_argument("--output_file", default="run.sh")
    parser.add_argument("--no_cache", action="store_true")
    
    return parser.parse_args()


def main(args):
    with open(args.output_file, "w") as f:
        for key, value in task_dict.items():
            cmd = f"python main.py --model {args.model} --model_args pretrained={args.model_args} --device=cuda:0 --tasks {key} --model_name {args.model_name} --data_path {args.data_path}"
            
            task_list = ','.join(value)
            cmd += f" --task_list {task_list}"
            
            if args.prompt_wrapper:
                cmd += f" --prompt_wrapper {args.prompt_wrapper}"
            
            if args.no_cache:
                cmd += f" --no_cache"
                
            f.write(f"{cmd}\n")
            
            
if __name__ == "__main__":
    args = parse_args()
    main(args)