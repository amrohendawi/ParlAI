#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
SeeKeR Search Decision Tasks.
"""
from typing import Optional

from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser
from parlai.core.teachers import MultiTaskTeacher
import parlai.tasks.wizard_of_internet.agents as woi
import parlai.tasks.squad.agents as squad
import parlai.tasks.triviaqa.agents as triviaqa
import parlai.tasks.msc.agents as msc

import parlai.utils.logging as logging

import projects.seeker.tasks.mutators  # type: ignore


class WoiSearchDecisionTeacher(woi.DefaultTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(
            [
                'flatten',
                'woi_dropout_retrieved_docs',
                'woi_maybe_generate_search_query_mutator',
                'woi_pop_documents_mutator',
                'skip_retrieval_mutator',
            ]
        )
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = 'WoiSearchDecisionTeacher'


class SquadSearchDecisionTeacher(squad.OpensquadTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(
            ['do_generate_search_query_mutator', 'skip_retrieval_mutator']
        )
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = 'SquadSearchDecisionTeacher'


class TriviaQASearchDecisionTeacher(triviaqa.NoEvidenceWebTeacher):
    def __init__(self, opt, shared=None):
        mutators = '+'.join(
            ['do_generate_search_query_mutator', 'skip_retrieval_mutator']
        )
        if opt.get('mutators'):
            mutators = '+'.join([mutators, opt['mutators']])
        logging.warning(f'overriding mutators to {mutators}')
        opt['mutators'] = mutators
        super().__init__(opt, shared)
        self.id = 'TriviaQASearchDecisionTeacher'


def get_dialogue_task_mutators(opt: Opt) -> str:
    """
    Set the mutators appropriately for the dialogue tasks.
    """
    mutators = '+'.join(
        [
            'flatten',
            'skip_retrieval_mutator',
            'bst_tasks_maybe_generate_search_query_mutator',
        ]
    )
    if opt.get('mutators'):
        mutators = '+'.join([mutators, opt['mutators']])
    logging.warning(f'overriding mutators to {mutators}')
    return mutators


class MSCSearchDecisionTeacher(msc.DefaultTeacher):
    def __init__(self, opt, shared=None):
        opt['mutators'] = get_dialogue_task_mutators(opt)
        opt['include_session1'] = False
        super().__init__(opt, shared)
        self.id = 'MSCSearchDecisionTeacher'


class SearchDecisionTeacher(MultiTaskTeacher):
    @classmethod
    def add_cmdline_args(
        cls, parser: ParlaiParser, partial_opt: Optional[Opt] = None
    ) -> ParlaiParser:
        WoiSearchDecisionTeacher.add_cmdline_args(parser, partial_opt)
        SquadSearchDecisionTeacher.add_cmdline_args(parser, partial_opt)
        TriviaQASearchDecisionTeacher.add_cmdline_args(parser, partial_opt)
        MSCSearchDecisionTeacher.add_cmdline_args(parser, partial_opt)
        return parser

    def __init__(self, opt, shared=None):
        tasks = [
            f"projects.seeker.tasks.search_decision:{teacher}"
            for teacher in [
                'WoiSearchDecisionTeacher',
                'SquadSearchDecisionTeacher',
                'TriviaQASearchDecisionTeacher',
                'MSCSearchDecisionTeacher',
            ]
        ]
        opt['task'] = ','.join(tasks)
        super().__init__(opt, shared)


class DefaultTeacher(SearchDecisionTeacher):
    pass
