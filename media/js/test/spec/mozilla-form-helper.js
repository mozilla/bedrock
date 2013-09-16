/* Base JS unit test spec for bedrock global.js
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe("mozilla-form-helper.js", function() {

  describe('Mozilla.FormHelper.displayErrors', function() {
    // form html
    var form_html = '<form id="testForm">' +
        '<div class="field"><label for="email">Email</label><input type="email" required="required" name="email" id="email"></div>' +
        '<div class="field"><label for="name">Name</label><input type="text" required="required" name="name" id="name"></div>' +
        '<div class="field"><label for="phone">Phone</label><input type="tel" name="phone" id="phone"></div>' +
        '</form>';

    // error objects to be used on the form
    var errors = {
      'email': 'Email is required',
      'name': 'Name is required'
    };

    var email_errors = {
      'email': 'Email is required'
    };

    beforeEach(function () {
      //create an HTML fixture to test against
      $('<div id="testDisplayFormErrors">' + form_html + '</div>').appendTo('body');
    });

    afterEach(function(){
      // Tidy up after each test
      $('#testDisplayFormErrors').remove();
    });

    it("should display error for name and email", function() {
      Mozilla.FormHelper.displayErrors(errors);

      var error_count = $('label[for="email"]').prev('.errorlist').length;
      error_count += $('label[for="name"]').prev('.errorlist').length;

      expect(error_count).toBe(2);
    });

    it("should display error for email only", function() {
      Mozilla.FormHelper.displayErrors(email_errors);

      expect($('.errorlist').length).toBe(1);
    });

    it("should display one error after displaying two errors", function() {
      // adds two error messages
      Mozilla.FormHelper.displayErrors(errors);
      // mimic re-submission of form with only email error
      Mozilla.FormHelper.displayErrors(email_errors);

      expect($('.errorlist').length).toBe(1);
    });

    describe("form in modal with duplicate field ids", function() {
      beforeEach(function() {
        // add form again to DOM - mimic modal that duplicates markup
        $('<div id="testModal">' + form_html + '</div>').appendTo('body');
      });

      afterEach(function() {
        $('#testModal').remove();
      });

      it("should display errors in modal form", function() {
        var modalForm = $('form')[1];
        Mozilla.FormHelper.displayErrors(errors, modalForm);
        expect($(modalForm).find('.errorlist').length).toBe(2);
      });

      it("should not display errors in modal form", function() {
        var modalForm = $('form')[1];
        Mozilla.FormHelper.displayErrors(errors);
        expect($(modalForm).find('.errorlist').length).toBe(0);
      });
    });
  });

});
