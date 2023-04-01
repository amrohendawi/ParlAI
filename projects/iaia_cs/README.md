## Intent-Aware Internet-Augmented Conversational Search (IAIA-CS)
- IAIA-CS is a modular Language Model (LM) similar to Seeker but fine-tuned to model its awareness of the intent of the user and the context of the conversation.

- The method is a single transformer which is called iteratively to generate: (i) a search query, (ii)  a knowledge sequence, (iii) and a final response.
- When applied to knowledge-seeking dialogues, it is superior to [SeeKer](https://arxiv.org/abs/2203.13224) and [GPT3](https://arxiv.org/abs/2005.14165) in terms of knowledgeability, engagingness, and awareness of the context of the conversation.
- When applied to language modeling, it hallucinates less and is more topical than either [GPT2](https://arxiv.org/abs/2005.14165) or [GPT3](https://arxiv.org/abs/2005.14165).


## Results

#### Training

The base models for SeeKeR LM are GPT2 models. So, the following commands (with interchangeable values for `--gpt2-size medium/large/xl`, and assuming we generated data with the above command and set `--save-dir /path/to/savedir`):


```shell
python -m parlai.scripts.multiprocessing_train \
-t projects.iaia_cs.tasks.lm:KnowledgeTeacher,projects.iaia_cs.tasks.lm:ResponseTeacher,projects.iaia_cs.tasks.lm:SearchQueryTeacher \
--root-dir /path/to/savedir/valid_split_0.5_f1_overlap --multitask-weights 2,2,1 \
--gpt2-size medium --text-truncate 896 --truncate 896 --label-truncate 128 --n-docs 5 \
--model projects.iaia_cs.agents.gpt2_seeker:GPT2ComboGpt2GoldDocumentAgent \
--batchsize 1 --fp16 True --optimizer adam --warmup-updates 500 --update-freq 1 \
--gradient-clip 1.0 --learningrate 7e-06 --lr-scheduler reduceonplateau --skip-generation True \
--ddp-backend zero2 -lstep 50 --metrics all -vp 5 -tstep 300000 -vmt ppl -vmm min -vstep 1000 \
--save-after-valid True --model-file /tmp/my_seeker_lm_model
``` 