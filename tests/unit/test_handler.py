import json
import pytest

from header_add import app


@pytest.fixture()
def cf_event():
    """ Generates CloudFront Event"""

    return {
    "Records": [
        {
            "cf": {
                "config": {
                    "distributionDomainName": "d123.cloudfront.net",
                    "distributionId": "EDFDVBD6EXAMPLE",
                    "eventType": "viewer-response",
                    "requestId": "xGN7KWpVEmB9Dp7ctcVFQC4E-nrcOcEKS3QyAez--06dV7TEXAMPLE=="
                },
                "request": {
                    "clientIp": "2001:0db8:85a3:0:0:8a2e:0370:7334",
                    "method": "GET",
                    "uri": "/picture.jpg",
                    "querystring": "size=large",
                    "headers": {
                        "host": [
                            {
                                "key": "Host",
                                "value": "d111111abcdef8.cloudfront.net"
                            }
                        ],
                        "user-agent": [
                            {
                                "key": "User-Agent",
                                "value": "curl/7.18.1"
                            }
                        ]
                    }
                },
                "response": {
                    "status": "200",
                    "statusDescription": "OK",
                    "headers": {
                        "server": [
                            {
                                "key": "Server",
                                "value": "MyCustomOrigin"
                            }
                        ],
                        "set-cookie": [
                            {
                                "key": "Set-Cookie",
                                "value": "theme=light"
                            },
                            {
                                "key": "Set-Cookie",
                                "value": "sessionToken=abc123; Expires=Wed, 09 Jun 2021 10:18:14 GMT"
                            }
                        ]
                    }
                }
            }
        }
    ]
}

def test_lambda_handler(cf_event):

    ret = app.lambda_handler(cf_event, "") # second arg is empty context
    print(ret)
    assert ret["status"] == '200'
    assert ret["statusDescription"] == "OK"

    assert ret["headers"]["strict-transport-security"][0]["key"] == "Strict-Transport-Security"
    assert ret["headers"]["strict-transport-security"][0]["value"] == "max-age=63072000; includeSubdomains; preload"

    assert ret["headers"]["content-security-policy"][0]["key"] == "Content-Security-Policy"
    assert ret["headers"]["content-security-policy"][0]["value"] == "default-src 'none'; img-src '*.imgur.com'; script-src 'self'; style-src 'self'; object-src 'none'"

    assert ret["headers"]["x-content-type-options"][0]["key"] == "X-Content-Type-Options"
    assert ret["headers"]["x-content-type-options"][0]["value"] == "nosniff"

    assert ret["headers"]["x-frame-options"][0]["key"] == "X-Frame-Options"
    assert ret["headers"]["x-frame-options"][0]["value"] == "DENY"

    assert ret["headers"]["x-xss-protection"][0]["key"] == "X-XSS-Protection"
    assert ret["headers"]["x-xss-protection"][0]["value"] == "1; mode=block"

    assert ret["headers"]["referrer-policy"][0]["key"] == "Referrer-Policy"
    assert ret["headers"]["referrer-policy"][0]["value"] == "same-origin"

    assert ret["headers"]["cache-control"][0]["key"] == "Cache-Control"
    assert ret["headers"]["cache-control"][0]["value"] == "max-age=604800"
