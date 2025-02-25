# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the issue_tracker_utils module."""

import unittest

from clusterfuzz._internal.datastore import data_types
from clusterfuzz._internal.issue_management import issue_tracker
from clusterfuzz._internal.issue_management import issue_tracker_utils
from clusterfuzz._internal.issue_management import monorail
from clusterfuzz._internal.tests.test_libs import helpers as test_helpers


class IssueTrackerUtilsUrlTest(unittest.TestCase):
  """Issue tracker utils tests for URL handling methods."""

  def setUp(self):
    test_helpers.patch(self, [
        'clusterfuzz._internal.issue_management.issue_tracker_utils.'
        'get_issue_tracker_for_testcase',
        'clusterfuzz._internal.issue_management.issue_tracker.IssueTracker.issue_url',
    ])

  def test_get_issue_url(self):
    """Basic test for a case when testcase is associated with a bug."""
    testcase = data_types.Testcase()
    testcase.bug_information = '1337'

    test_issue_tracker = issue_tracker.IssueTracker()
    self.mock.get_issue_tracker_for_testcase.return_value = test_issue_tracker

    issue_tracker_utils.get_issue_url(testcase)
    self.mock.issue_url.assert_called_with(test_issue_tracker, '1337')

  def test_get_issue_url_group_bug(self):
    """Test for a case when testcase is associated with a group bug."""
    testcase = data_types.Testcase()
    testcase.group_bug_information = 31337

    test_issue_tracker = issue_tracker.IssueTracker()
    self.mock.get_issue_tracker_for_testcase.return_value = test_issue_tracker

    issue_tracker_utils.get_issue_url(testcase)
    self.mock.issue_url.assert_called_with(test_issue_tracker, '31337')

  def test_get_issue_url_no_bug(self):
    """Test for a case when testcase has no bugs associated with it."""
    testcase = data_types.Testcase()

    test_issue_tracker = issue_tracker.IssueTracker()
    self.mock.get_issue_tracker_for_testcase.return_value = test_issue_tracker

    issue_tracker_utils.get_issue_url(testcase)
    self.assertEqual(0, self.mock.issue_url.call_count)

  def test_get_issue_tracker(self):
    # pylint: disable=protected-access
    """Test for get issue tracker."""
    test_helpers.patch(self, [
        'clusterfuzz._internal.config.local_config.IssueTrackerConfig.get',
        'clusterfuzz._internal.issue_management.monorail._get_issue_tracker_manager_for_project'
    ])
    self.mock.get.return_value = {'type': 'monorail'}
    self.mock._get_issue_tracker_manager_for_project.return_value = 'test_icm'
    issue_tracker_utils._ISSUE_TRACKER_CONSTRUCTORS = {
        'monorail': monorail.get_issue_tracker
    }

    constructor = issue_tracker_utils.get_issue_tracker()
    self.assertIsNotNone(constructor)
