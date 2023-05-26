/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const TrackBeginCheckout = {};

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
            item.category,
            item.name,
            item.variant,
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
 * @param {string} id // this is the FxA parameter that starts with "price_"
 * @param {string} plan // example: email
 * @param {string} product // example: relay
 * @param {string} period // monthly or yearly
 * @param {int} price
 * @param {string} currency
 * @param {int} discount // monetary value of discount (optional)
 * @returns {Object}
 */
TrackBeginCheckout.getEventObject = (
    item_id,
    product,
    plan,
    period,
    price,
    currency,
    discount = 0
) => {
    const itemObj = {};
    itemObj['item_id'] = item_id;
    itemObj['item_name'] = plan;
    itemObj['item_category'] = product;
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
    product,
    plan,
    period,
    price,
    discount,
    currency
) => {
    const eventObject = TrackBeginCheckout.getEventObject(
        item_id,
        product,
        plan,
        period,
        price,
        discount,
        currency
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
