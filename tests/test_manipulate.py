class TestManipulate:
    config = r"""
        tasks:

          test_1:
            mock:
              - {title: 'abc FOO'}
            manipulate:
              - title:
                  replace:
                    regexp: FOO
                    format: BAR

          test_2:
            mock:
              - {title: '1234 abc'}
            manipulate:
              - title:
                  extract: \d+\s*(.*)

          test_multiple_edits:
            mock:
              - {title: 'abc def'}
            manipulate:
              - title:
                  replace:
                    regexp: abc
                    format: "123"
              - title:
                  extract: \d+\s+(.*)

          test_phase:
            mock:
              - {title: '1234 abc'}
            manipulate:
              - title:
                  phase: metainfo
                  extract: \d+\s*(.*)

          test_remove:
            mock:
              - {title: 'abc', description: 'def'}
            manipulate:
              - description: { remove: yes }

          test_replace_with_group:
            mock:
              - {title: '1234-7890'}
            manipulate:
              - title:
                  replace:
                    regexp: (1234)\-(7890)
                    format: 'e\2'

          test_erase_regex_single:
            mock:
              - {title: 'Some crap foo'}
            manipulate:
              - title:
                  erase:
                    - "^some.crap."

          test_erase_regex_multiple:
            mock:
              - {title: 'Some crap more junk foo bar'}
            manipulate:
              - title:
                  erase:
                    - "^some.crap."
                    - "more.junk."

          test_erase_regex_case_insensitive:
            mock:
              - {title: 'PREFIX: SOME CRAP the title'}
            manipulate:
              - title:
                  erase:
                    - "^prefix:"
                    - "some.crap."

          test_erase_regex_no_match:
            mock:
              - {title: 'Clean title'}
            manipulate:
              - title:
                  erase:
                    - "^notfound"
                    - "alsomissing"

          test_erase_regex_empty_result:
            mock:
              - {title: 'completely removed text'}
            manipulate:
              - title:
                  erase:
                    - ".*"

          test_erase_regex_with_other_operations:
            mock:
              - {title: 'PREFIX: some crap GOOD TITLE suffix'}
            manipulate:
              - title:
                  erase:
                    - "^prefix:"
                    - "some.crap."
              - title:
                  replace:
                    regexp: "suffix$"
                    format: ""

          test_erase_title_failure:
            mock:
              - {title: 'temp title'}
            manipulate:
              - title:
                  erase:
                    - ".*"
    """

    def test_replace(self, execute_task):
        task = execute_task('test_1')
        assert task.find_entry('entries', title='abc BAR'), 'replace failed'

    def test_replace_with_group(self, execute_task):
        task = execute_task('test_replace_with_group')
        entry = task.all_entries[0]
        assert entry['title'] == 'e7890', 'Title should have been {} but was {}'.format(
            'e7890',
            entry['title'],
        )

    def test_extract(self, execute_task):
        task = execute_task('test_2')
        assert task.find_entry('entries', title='abc'), 'extract failed'

    def test_multiple_edits(self, execute_task):
        task = execute_task('test_multiple_edits')
        assert task.find_entry('entries', title='def'), 'multiple edits on 1 field failed'

    def test_phase(self, execute_task):
        task = execute_task('test_phase')
        assert task.find_entry('entries', title='abc'), 'extract failed at metainfo phase'

    def test_remove(self, execute_task):
        task = execute_task('test_remove')
        assert 'description' not in task.find_entry('entries', title='abc'), 'remove failed'

    def test_erase_regex_single(self, execute_task):
        task = execute_task('test_erase_regex_single')
        assert task.find_entry('entries', title='foo'), 'single regex erase failed'

    def test_erase_regex_multiple(self, execute_task):
        task = execute_task('test_erase_regex_multiple')
        assert task.find_entry('entries', title='foo bar'), 'multiple regex erase failed'

    def test_erase_regex_case_insensitive(self, execute_task):
        task = execute_task('test_erase_regex_case_insensitive')
        assert task.find_entry('entries', title='the title'), 'case insensitive regex erase failed'

    def test_erase_regex_no_match(self, execute_task):
        task = execute_task('test_erase_regex_no_match')
        assert task.find_entry('entries', title='Clean title'), (
            'no match regex erase changed title when it should not have'
        )

    def test_erase_regex_empty_result(self, execute_task):
        task = execute_task('test_erase_regex_empty_result')
        # Entry should be failed when title becomes empty
        assert len(task.failed) == 1, 'entry should have been failed when title became empty'
        assert 'Title became empty after erase operation' in task.failed[0]['reason']

    def test_erase_regex_with_other_operations(self, execute_task):
        task = execute_task('test_erase_regex_with_other_operations')
        assert task.find_entry('entries', title='GOOD TITLE'), (
            'regex erase combined with replace failed'
        )

    def test_erase_title_failure(self, execute_task):
        task = execute_task('test_erase_title_failure')
        # Entry should be failed when title becomes empty
        assert len(task.failed) == 1, 'entry should have been failed when title became empty'
        assert 'Title became empty after erase operation' in task.failed[0]['reason']
        assert len(task.entries) == 0, 'no entries should remain when title is completely erased'
