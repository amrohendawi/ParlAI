#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
SeeKeR Knowledge Tasks.
"""
from typing import Optional, List
from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser
from parlai.core.teachers import MultiTaskTeacher
import parlai.tasks.msc.agents as msc
import parlai.tasks.wizard_of_internet.agents as woi
import parlai.tasks.squad.agents as squad
import parlai.tasks.ms_marco.agents as ms_marco
import parlai.tasks.triviaqa.agents as triviaqa
import parlai.tasks.natural_questions.agents as nq

import parlai.utils.logging as logging

import projects.seeker.tasks.mutators  # type: ignore


class WoiKnowledgeTeacher(woi.DefaultTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(self.get_special_mutators())
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = "WoiKnowledgeTeacher"

    def get_special_mutators(self) -> List[str]:
        return [
            'flatten',
            'woi_filter_no_passage_used',
            'woi_checked_sentence_as_label',
            'woi_chunk_retrieved_docs',
            'woi_dropout_retrieved_docs',
            'woi_filter_selected_knowledge_in_retrieved_docs',
        ]


class MsMarcoKnowledgeTeacher(ms_marco.DefaultTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(self.get_special_mutators())
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = "MsMarcoKnowledgeTeacher"

    def get_special_mutators(self) -> List[str]:
        return [
            'ms_marco_filter_has_answer',
            'ms_marco_create_fid_docs',
            'ms_marco_find_selected_sentence_for_knowledge',
            'ms_marco_to_woi',
            'woi_chunk_retrieved_docs',
            'add_selected_sentences_mutator',
        ]


class SquadKnowledgeTeacher(squad.DefaultTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(self.get_special_mutators())
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = "SquadKnowledgeTeacher"

    def get_special_mutators(self) -> List[str]:
        return [
            'squad_to_woi',
            'woi_chunk_retrieved_docs',
            'add_selected_sentences_mutator',
        ]


class TriviaQAKnowledgeTeacher(triviaqa.DefaultTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(self.get_special_mutators())
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = "TriviaQAKnowledgeTeacher"

    def get_special_mutators(self) -> List[str]:
        return [
            'triviaqa_to_woi',
            'woi_chunk_retrieved_docs',
            'add_selected_sentences_mutator',
        ]


class NQOpenKnowledgeTeacher(nq.NaturalQuestionsOpenTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(self.get_special_mutators())
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = "NQOpenKnowledgeTeacher"

    def get_special_mutators(self) -> List[str]:
        return [
            'nqopen_to_woi',
            'woi_chunk_retrieved_docs',
            'add_selected_sentences_mutator',
        ]


def get_dialogue_task_mutators(opt: Opt) -> str:
    """
    Set the mutators appropriately for the dialogue tasks.
    """
    mutators = '+'.join(
        ['flatten', 'extract_entity_for_knowledge_model', 'skip_retrieval_mutator']
    )
    if opt.get('mutators'):
        mutators = '+'.join([mutators, opt['mutators']])
    logging.warning(f'overriding mutators to {mutators}')
    return mutators


class MSCKnowledgeTeacher(msc.DefaultTeacher):
    def __init__(self, opt, shared=None):
        opt['mutators'] = self.get_special_mutators(opt)
        opt['include_session1'] = False
        super().__init__(opt, shared)
        self.id = 'MSCKnowledgeTeacher'

    def get_special_mutators(self, opt):
        return get_dialogue_task_mutators(opt)


class MSCKnowledgeOverlapTeacher(msc.DefaultTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(
            [
                'flatten',
                'msc_find_selected_sentence_knowledge',
                'add_retrieved_documents_mutator',
                'skip_retrieval_mutator',
            ]
        )
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['include_session1'] = False
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = 'MSCKnowledgeOverlapTeacher'


class KnowledgeTeacher(MultiTaskTeacher):
    @classmethod
    def add_cmdline_args(
            cls, parser: ParlaiParser, partial_opt: Optional[Opt] = None
    ) -> ParlaiParser:
        WoiKnowledgeTeacher.add_cmdline_args(parser, partial_opt)
        MsMarcoKnowledgeTeacher.add_cmdline_args(parser, partial_opt)
        SquadKnowledgeTeacher.add_cmdline_args(parser, partial_opt)
        TriviaQAKnowledgeTeacher.add_cmdline_args(parser, partial_opt)
        NQOpenKnowledgeTeacher.add_cmdline_args(parser, partial_opt)
        MSCKnowledgeTeacher.add_cmdline_args(parser, partial_opt)
        MSCKnowledgeOverlapTeacher.add_cmdline_args(parser, partial_opt)
        return parser

    def __init__(self, opt, shared=None):
        tasks = [
            f"projects.seeker.tasks.knowledge:{teacher}"
            for teacher in [
                'WoiKnowledgeTeacher',
                'MsMarcoKnowledgeTeacher',
                'SquadKnowledgeTeacher',
                'TriviaQAKnowledgeTeacher',
                'NQOpenKnowledgeTeacher',
                'MSCKnowledgeTeacher',
                'MSCKnowledgeOverlapTeacher',
            ]
        ]
        opt['task'] = ','.join(tasks)
        super().__init__(opt, shared)


class DefaultTeacher(KnowledgeTeacher):
    pass
