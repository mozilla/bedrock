/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const TrackBeginCheckout = {};
if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

/**
 */
TrackBeginCheckout.handleLinkWithItemData = (event) => {
    try {
        const t = event.target;
        let item = t.dataset.gaItem;
        item = item.replace(/'/gi, '"');
        item = JSON.parse(item);
        TrackBeginCheckout.getEventObjectAndSend(
            item.id,
            item.brand,
            item.plan,
            item.period,
            item.price,
            item.currency,
            item.discount
        );
    } catch (error) {
        return;
    }
};

/**
 * Create the begin_checkout GA event object
 * @param {string} id // Stripe plan ID  - this is the FxA parameter that starts with "price_"
 * @param {string} brand // example: relay
 * @param {string} plan // example: email
 * @param {string} period // monthly or yearly
 * @param {int} price
 * @param {string} currency
 * @param {int} discount // monetary value of discount (optional)
 * @returns {Object}
 */
TrackBeginCheckout.getEventObject = (
    item_id,
    brand,
    plan,
    period,
    price,
    currency,
    discount = 0
) => {
    const itemObj = {};
    itemObj['item_id'] = item_id;
    itemObj['item_brand'] = brand;
    itemObj['item_name'] = plan;
    itemObj['item_variant'] = period;
    itemObj['price'] = price;
    itemObj['discount'] = discount;

    const eventObj = {
        event: 'begin_checkout',
        ecommerce: {
            currency: currency,
            value: price,
            items: [itemObj]
        }
    };

    return eventObj;
};

/**
 * Gets a properly formatted GA begin_checkout event and then sends it to the data layer
 * @param {Object} - purchase details formatted into a begin_checkout event
 */
TrackBeginCheckout.getEventObjectAndSend = (
    item_id,
    brand,
    plan,
    period,
    price,
    currency,
    discount
) => {
    const eventObject = TrackBeginCheckout.getEventObject(
        item_id,
        brand,
        plan,
        period,
        price,
        currency,
        discount
    );
    TrackBeginCheckout.sendEvent(eventObject);
};

/**
 * Sends a GA event to the data layer
 * @param {Object} - purchase details formatted into a begin_checkout event
 */
TrackBeginCheckout.sendEvent = (eventObject) => {
    window.dataLayer.push(eventObject);
};

export default TrackBeginCheckout;
