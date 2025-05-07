$(document).ready(function () {
    $('#convert-form').submit(function (e) {
        e.preventDefault();
        const formData = {
            amount: $('input[name="amount"]').val(),
            base: $('input[name="base"]').val().toUpperCase(),
            target: $('input[name="target"]').val().toUpperCase()
        };

        $.ajax({
            url: '/api/convert',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function (response) {
                $('#convert-result')
                    .removeClass('d-none alert-danger')
                    .addClass('alert-info')
                    .text(`Result: ${response.converted}`);
            },
            error: function (xhr) {
                $('#convert-result')
                    .removeClass('d-none alert-info')
                    .addClass('alert-danger')
                    .text(xhr.responseJSON?.error || 'Error occurred');
            }
        });
    });

    $('#update-rates').click(function () {
        const base = $('input[name="update-target"]').val().toUpperCase() || 'USD';
        const $button = $(this);
        const $spinner = $('#spinner');
    
        $button.prop('disabled', true).contents().last()[0].textContent = 'Updating...';
        $spinner.removeClass('d-none');
    
        $.ajax({
            url: '/api/update_rates',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ base: base }),
            success: function (response) {
                $('#convert-result')
                    .removeClass('d-none alert-danger')
                    .addClass('alert-info')
                    .text(response.message);
                fetchLastUpdate();
            },
            error: function (xhr) {
                $('#convert-result')
                    .removeClass('d-none alert-info')
                    .addClass('alert-danger')
                    .text(xhr.responseJSON?.error || 'Failed to update rates');
            },
            complete: function () {
                $spinner.addClass('d-none');
                $button.prop('disabled', false).contents().last()[0].textContent = 'Update Rates';
            }
        });
    });
    

    function fetchLastUpdate() {
        $.get('/api/last_update', function (data) {
            $('#last-updated').text('Last update: ' + data.last_update);
        });
    }

    fetchLastUpdate();
});
