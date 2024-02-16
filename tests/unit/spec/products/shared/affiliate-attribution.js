/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

import AffiliateAttribution from '../../../../../media/js/products/shared/affiliate-attribution.es6.js';
import FxaProductButton from '../../../../../media/js/base/fxa-product-button.es6.js';

describe('affiliate-attribution.es6.js', function () {
    const _cjEventParam = '09d8676b716a11ec831e01500a18050e';
    const _cjmsCookieValue = '365fd94a-c507-43b3-b867-034f786d2cee';
    const _endpoint = 'https://stage.cjms.nonprod.cloudops.mozgcp.net/aic';
    const _deviceIDValue = '848377ff6e3e4fc982307a316f4ca3d6';
    const _flowBeginTimeValue = '1573052386673';
    const _flowIDValue =
        '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1';
    const _flowParamString = `&device_id=${_deviceIDValue}&flow_begin_time=${_flowBeginTimeValue}&flow_id=${_flowIDValue}`;
    const responseData = {
        aic_id: _cjmsCookieValue,
        expires: 1648893757
    };

    describe('init', function () {
        describe('succcess', function () {
            beforeEach(function () {
                const mockResponse = new window.Response(
                    JSON.stringify(responseData),
                    {
                        status: 200,
                        headers: {
                            'Content-type': 'application/json'
                        }
                    }
                );

                spyOn(window, 'fetch').and.returnValue(
                    window.Promise.resolve(mockResponse)
                );
            });

            it('should send flow ID and CJ event param to micro service and then set a marketing cookie', function () {
                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(true);
                spyOn(AffiliateAttribution, 'getCJEventParam').and.returnValue(
                    _cjEventParam
                );
                spyOn(AffiliateAttribution, 'getCJMSEndpoint').and.returnValue(
                    _endpoint
                );
                spyOn(
                    AffiliateAttribution,
                    'hasMarketingCookie'
                ).and.returnValue(false);
                spyOn(FxaProductButton, 'init').and.resolveTo(_flowParamString);
                spyOn(AffiliateAttribution, 'fetch').and.callThrough();
                spyOn(
                    AffiliateAttribution,
                    'setMarketingCookie'
                ).and.callThrough();
                spyOn(window.Mozilla.Cookies, 'setItem');
                return AffiliateAttribution.init().then(() => {
                    expect(AffiliateAttribution.fetch).toHaveBeenCalledWith(
                        _flowIDValue,
                        _cjEventParam
                    );

                    expect(window.fetch).toHaveBeenCalledWith(_endpoint, {
                        method: 'POST',
                        headers: {
                            Accept: 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: `{"flow_id":"${_flowIDValue}","cj_id":"${_cjEventParam}"}`
                    });

                    expect(
                        AffiliateAttribution.setMarketingCookie
                    ).toHaveBeenCalledWith(
                        responseData.aic_id,
                        responseData.expires
                    );

                    expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                        'moz-cj-affiliate',
                        _cjmsCookieValue,
                        jasmine.any(String),
                        '/',
                        null,
                        false,
                        'lax'
                    );
                });
            });

            it('should send marketing cookie ID along with flow ID and CJ event params if cookie already exists', function () {
                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(true);
                spyOn(AffiliateAttribution, 'getCJEventParam').and.returnValue(
                    _cjEventParam
                );
                spyOn(AffiliateAttribution, 'getCJMSEndpoint').and.returnValue(
                    _endpoint
                );
                spyOn(
                    AffiliateAttribution,
                    'hasMarketingCookie'
                ).and.returnValue(true);
                spyOn(
                    AffiliateAttribution,
                    'getMarketingCookie'
                ).and.returnValue(_cjmsCookieValue);
                spyOn(FxaProductButton, 'init').and.resolveTo(_flowParamString);
                spyOn(AffiliateAttribution, 'fetch').and.callThrough();
                spyOn(
                    AffiliateAttribution,
                    'setMarketingCookie'
                ).and.callThrough();
                spyOn(window.Mozilla.Cookies, 'setItem');
                return AffiliateAttribution.init().then(() => {
                    expect(AffiliateAttribution.fetch).toHaveBeenCalledWith(
                        _flowIDValue,
                        _cjEventParam,
                        _cjmsCookieValue
                    );

                    expect(window.fetch).toHaveBeenCalledWith(
                        `${_endpoint}/${_cjmsCookieValue}`,
                        {
                            method: 'PUT',
                            headers: {
                                Accept: 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: `{"flow_id":"${_flowIDValue}","cj_id":"${_cjEventParam}"}`
                        }
                    );

                    expect(
                        AffiliateAttribution.setMarketingCookie
                    ).toHaveBeenCalledWith(
                        responseData.aic_id,
                        responseData.expires
                    );

                    expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                        'moz-cj-affiliate',
                        _cjmsCookieValue,
                        jasmine.any(String),
                        '/',
                        null,
                        false,
                        'lax'
                    );
                });
            });

            it('should send existing marketing cookie ID along with only a flow ID if no CJ event param exists', function () {
                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(true);
                spyOn(AffiliateAttribution, 'getCJEventParam').and.returnValue(
                    false
                );
                spyOn(AffiliateAttribution, 'getCJMSEndpoint').and.returnValue(
                    _endpoint
                );
                spyOn(
                    AffiliateAttribution,
                    'hasMarketingCookie'
                ).and.returnValue(true);
                spyOn(
                    AffiliateAttribution,
                    'getMarketingCookie'
                ).and.returnValue(_cjmsCookieValue);
                spyOn(FxaProductButton, 'init').and.resolveTo(_flowParamString);
                spyOn(AffiliateAttribution, 'fetch').and.callThrough();
                spyOn(
                    AffiliateAttribution,
                    'setMarketingCookie'
                ).and.callThrough();
                spyOn(window.Mozilla.Cookies, 'setItem');
                return AffiliateAttribution.init().then(() => {
                    expect(AffiliateAttribution.fetch).toHaveBeenCalledWith(
                        _flowIDValue,
                        null,
                        _cjmsCookieValue
                    );

                    expect(window.fetch).toHaveBeenCalledWith(
                        `${_endpoint}/${_cjmsCookieValue}`,
                        {
                            method: 'PUT',
                            headers: {
                                Accept: 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: `{"flow_id":"${_flowIDValue}"}`
                        }
                    );

                    expect(
                        AffiliateAttribution.setMarketingCookie
                    ).toHaveBeenCalledWith(
                        responseData.aic_id,
                        responseData.expires
                    );

                    expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                        'moz-cj-affiliate',
                        _cjmsCookieValue,
                        jasmine.any(String),
                        '/',
                        null,
                        false,
                        'lax'
                    );
                });
            });
        });

        describe('failure', function () {
            it('should return false if browser requirements are not satisfied', function () {
                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(false);
                expect(AffiliateAttribution.init()).toBeFalse();
            });

            it('should reject if no API endpoint is found', function () {
                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(true);
                spyOn(AffiliateAttribution, 'getCJEventParam').and.returnValue(
                    _cjEventParam
                );
                spyOn(AffiliateAttribution, 'getCJMSEndpoint').and.returnValue(
                    undefined
                );
                spyOn(FxaProductButton, 'init').and.resolveTo(_flowParamString);
                spyOn(window, 'fetch');
                spyOn(AffiliateAttribution, 'fetch').and.callThrough();
                return AffiliateAttribution.fetch().catch((reason) => {
                    expect(reason).toEqual('CJMS endpoint was not found.');
                    expect(window.fetch).not.toHaveBeenCalled();
                });
            });

            it('should reject if FxA flow params are undefined', function () {
                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(true);
                spyOn(AffiliateAttribution, 'getCJEventParam').and.returnValue(
                    _cjEventParam
                );
                spyOn(AffiliateAttribution, 'getCJMSEndpoint').and.returnValue(
                    _endpoint
                );
                spyOn(FxaProductButton, 'init').and.resolveTo(undefined);
                spyOn(window, 'fetch');
                return AffiliateAttribution.init().catch((reason) => {
                    expect(reason).toEqual('FxA flow params are undefined.');
                    expect(window.fetch).not.toHaveBeenCalled();
                });
            });

            it('should do a new POST if PUT fails with a 404', function () {
                const mock404Response = new window.Response(
                    JSON.stringify({}),
                    {
                        status: 404,
                        headers: {
                            'Content-type': 'application/json'
                        }
                    }
                );

                const mock200Response = new window.Response(
                    JSON.stringify(responseData),
                    {
                        status: 200,
                        headers: {
                            'Content-type': 'application/json'
                        }
                    }
                );

                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(true);
                spyOn(AffiliateAttribution, 'getCJEventParam').and.returnValue(
                    _cjEventParam
                );
                spyOn(AffiliateAttribution, 'getCJMSEndpoint').and.returnValue(
                    _endpoint
                );
                spyOn(
                    AffiliateAttribution,
                    'hasMarketingCookie'
                ).and.returnValue(true);
                spyOn(
                    AffiliateAttribution,
                    'getMarketingCookie'
                ).and.returnValue(_cjmsCookieValue);
                spyOn(FxaProductButton, 'init').and.resolveTo(_flowParamString);

                spyOn(window, 'fetch').and.returnValues(
                    window.Promise.resolve(mock404Response),
                    window.Promise.resolve(mock200Response)
                );

                return AffiliateAttribution.init().then(() => {
                    expect(window.fetch).toHaveBeenCalledTimes(2);
                    expect(window.fetch).toHaveBeenCalledWith(
                        'https://stage.cjms.nonprod.cloudops.mozgcp.net/aic/365fd94a-c507-43b3-b867-034f786d2cee',
                        {
                            method: 'PUT',
                            headers: {
                                Accept: 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: '{"flow_id":"75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1","cj_id":"09d8676b716a11ec831e01500a18050e"}'
                        }
                    );
                    expect(window.fetch).toHaveBeenCalledWith(
                        'https://stage.cjms.nonprod.cloudops.mozgcp.net/aic',
                        {
                            method: 'POST',
                            headers: {
                                Accept: 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: '{"flow_id":"75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1","cj_id":"09d8676b716a11ec831e01500a18050e"}'
                        }
                    );
                });
            });

            it('should delete marketing cookie if PUT fails with a 404 and there is no cjevent param', function () {
                const mock404Response = new window.Response(
                    JSON.stringify({}),
                    {
                        status: 404,
                        headers: {
                            'Content-type': 'application/json'
                        }
                    }
                );

                spyOn(
                    AffiliateAttribution,
                    'meetsRequirements'
                ).and.returnValue(true);
                spyOn(AffiliateAttribution, 'getCJEventParam').and.returnValue(
                    false
                );
                spyOn(AffiliateAttribution, 'getCJMSEndpoint').and.returnValue(
                    _endpoint
                );
                spyOn(
                    AffiliateAttribution,
                    'hasMarketingCookie'
                ).and.returnValue(true);
                spyOn(
                    AffiliateAttribution,
                    'getMarketingCookie'
                ).and.returnValue(_cjmsCookieValue);
                spyOn(AffiliateAttribution, 'removeMarketingCookie');
                spyOn(FxaProductButton, 'init').and.resolveTo(_flowParamString);

                spyOn(window, 'fetch').and.returnValue(
                    window.Promise.resolve(mock404Response)
                );

                return AffiliateAttribution.init().then(() => {
                    expect(window.fetch).toHaveBeenCalledTimes(1);
                    expect(window.fetch).toHaveBeenCalledWith(
                        'https://stage.cjms.nonprod.cloudops.mozgcp.net/aic/365fd94a-c507-43b3-b867-034f786d2cee',
                        {
                            method: 'PUT',
                            headers: {
                                Accept: 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: '{"flow_id":"75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1"}'
                        }
                    );
                    expect(
                        AffiliateAttribution.removeMarketingCookie
                    ).toHaveBeenCalled();
                });
            });
        });
    });

    describe('getCJEventParam', function () {
        it('should return a valid CJ event value', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                _cjEventParam
            );
            expect(AffiliateAttribution.getCJEventParam()).toEqual(
                _cjEventParam
            );
        });

        it('should return false if the event value is greater than 64 characters', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                _cjEventParam.repeat(5)
            );
            expect(AffiliateAttribution.getCJEventParam()).toBeFalse();
        });

        it('should return false if event value contains unsafe characters', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                '\\<$@/">'
            );
            expect(AffiliateAttribution.getCJEventParam()).toBeFalse();
        });

        it('should return false if event value contains unsafe encoded characters', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                '%5C%3C%24%40%2F%22%3E'
            );
            expect(AffiliateAttribution.getCJEventParam()).toBeFalse();
        });

        it('should always return a string when event value is valid', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                1234567890
            );
            expect(AffiliateAttribution.getCJEventParam()).toEqual(
                '1234567890'
            );
        });

        it('should return false when event value is undefined', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                'undefined'
            );
            expect(AffiliateAttribution.getCJEventParam()).toBeFalse();
        });
    });

    describe('optOut', function () {
        beforeEach(function () {
            const mockResponse = new window.Response(
                JSON.stringify(responseData),
                {
                    status: 200,
                    headers: {
                        'Content-type': 'application/json'
                    }
                }
            );

            spyOn(window, 'fetch').and.returnValue(
                window.Promise.resolve(mockResponse)
            );
        });

        it('should should overwrite existing flow parameters, set a preference cookie and remove marketing cookie', function () {
            spyOn(FxaProductButton, 'init').and.resolveTo(_flowParamString);
            spyOn(
                AffiliateAttribution,
                'setPreferenceCookie'
            ).and.callThrough();
            spyOn(
                AffiliateAttribution,
                'removeMarketingCookie'
            ).and.callThrough();
            spyOn(window.Mozilla.Cookies, 'setItem');
            spyOn(window.Mozilla.Cookies, 'removeItem');
            return AffiliateAttribution.optOut().then(() => {
                expect(FxaProductButton.init).toHaveBeenCalledWith(true);
                expect(
                    AffiliateAttribution.setPreferenceCookie
                ).toHaveBeenCalled();
                expect(
                    AffiliateAttribution.removeMarketingCookie
                ).toHaveBeenCalled();
                expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                    'moz-pref-cj-affiliate',
                    'reject',
                    jasmine.any(String),
                    '/',
                    null,
                    false,
                    'lax'
                );
                expect(window.Mozilla.Cookies.removeItem).toHaveBeenCalledWith(
                    'moz-cj-affiliate',
                    '/',
                    null,
                    false,
                    'lax'
                );
            });
        });
    });

    describe('shouldInitiateAttributionFlow', function () {
        it('should return true when preference cookie is not set', function () {
            spyOn(AffiliateAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(null);
            expect(
                AffiliateAttribution.shouldInitiateAttributionFlow()
            ).toBeTrue();
            expect(window.Mozilla.Cookies.getItem).toHaveBeenCalledWith(
                'moz-pref-cj-affiliate'
            );
        });

        it('should return true when preference cookie is set to "accept"', function () {
            spyOn(AffiliateAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue('accept');
            expect(
                AffiliateAttribution.shouldInitiateAttributionFlow()
            ).toBeTrue();
            expect(window.Mozilla.Cookies.getItem).toHaveBeenCalledWith(
                'moz-pref-cj-affiliate'
            );
        });

        it('should return false when preference cookie is set to "reject"', function () {
            spyOn(AffiliateAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue('reject');
            expect(
                AffiliateAttribution.shouldInitiateAttributionFlow()
            ).toBeFalse();
            expect(window.Mozilla.Cookies.getItem).toHaveBeenCalledWith(
                'moz-pref-cj-affiliate'
            );
        });

        it('should return false when requirements are not met', function () {
            spyOn(AffiliateAttribution, 'meetsRequirements').and.returnValue(
                false
            );
            expect(
                AffiliateAttribution.shouldInitiateAttributionFlow()
            ).toBeFalse();
        });
    });

    describe('shouldShowOptOutNotification', function () {
        it('should return true when a CJ event parameter is present', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                _cjEventParam
            );
            expect(
                AffiliateAttribution.shouldShowOptOutNotification()
            ).toBeTrue();
        });

        it('should return true when a marketing cookie is present', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                false
            );
            spyOn(AffiliateAttribution, 'hasPreferenceCookie').and.returnValue(
                false
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(true);
            expect(
                AffiliateAttribution.shouldShowOptOutNotification()
            ).toBeTrue();
            expect(window.Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
                'moz-cj-affiliate'
            );
        });

        it('should return false when neither CJ event parameter or marketing cookie are present', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                false
            );
            spyOn(AffiliateAttribution, 'hasPreferenceCookie').and.returnValue(
                false
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(false);
            expect(
                AffiliateAttribution.shouldShowOptOutNotification()
            ).toBeFalse();
        });

        it('should return false when preference cookie is set to "accept"', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                true
            );
            spyOn(AffiliateAttribution, 'hasMarketingCookie').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue('accept');
            expect(
                AffiliateAttribution.shouldShowOptOutNotification()
            ).toBeFalse();
            expect(window.Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
                'moz-pref-cj-affiliate'
            );
        });

        it('should return false when preference cookie is set to "reject"', function () {
            spyOn(AffiliateAttribution, 'getQueryStringParam').and.returnValue(
                true
            );
            spyOn(AffiliateAttribution, 'hasMarketingCookie').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue('reject');
            expect(
                AffiliateAttribution.shouldShowOptOutNotification()
            ).toBeFalse();
            expect(window.Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
                'moz-pref-cj-affiliate'
            );
        });
    });
});
