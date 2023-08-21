# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.                                                
                                                                                                                  
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance    
# with the License. A copy of the License is located at                                                             
                                                                                                                  
#     http://www.apache.org/licenses/LICENSE-2.0                                                                    
                                                                                                                  
# or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES 
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    
# and limitations under the License.

import json
import os
import sys

import pytest


@pytest.fixture(scope="function")
def stack_defaults():
    os.environ["SEEDFARMER_PROJECT_NAME"] = "test-project"
    os.environ["SEEDFARMER_DEPLOYMENT_NAME"] = "test-deployment"
    os.environ["SEEDFARMER_MODULE_NAME"] = "test-module"
    os.environ["SEEDFARMER_HASH"] = "xxxxxxxx"
    os.environ["SEEDFARMER_PARAMETER_INTERNET_ACCESSIBLE"] = "true"
    os.environ["CDK_DEFAULT_ACCOUNT"] = "111111111111"
    os.environ["CDK_DEFAULT_REGION"] = "us-east-1"

    # Unload the app import so that subsequent tests don't reuse
    if "app" in sys.modules:
        del sys.modules["app"]


def test_app(stack_defaults):
    import app  # noqa: F401


def test_internet_default(stack_defaults):
    del os.environ["SEEDFARMER_PARAMETER_INTERNET_ACCESSIBLE"]
    os.environ["SEEDFARMER_PARAMETER_INTERNET_ACCESSIBLE"] = "true"
    import app  # noqa: F401

    assert app.internet_accessible is True


def test_internet_bad_value(stack_defaults):
    del os.environ["SEEDFARMER_PARAMETER_INTERNET_ACCESSIBLE"]
    os.environ["SEEDFARMER_PARAMETER_INTERNET_ACCESSIBLE"] = "fsfadsfasdfsa"
    with pytest.raises(json.decoder.JSONDecodeError) as e:
        import app  # noqa: F401
    assert "JSONDecodeError" in str(e)


def test_internet_false(stack_defaults):
    del os.environ["SEEDFARMER_PARAMETER_INTERNET_ACCESSIBLE"]
    os.environ["SEEDFARMER_PARAMETER_INTERNET_ACCESSIBLE"] = "false"
    import app  # noqa: F401

    assert app.internet_accessible is False
