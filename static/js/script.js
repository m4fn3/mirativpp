$(function () {
    $('#login').on('click', function () {
        location.href = `/?token=` + $('#token').val()
    })
    $('#logout').on('click', function () {
        location.href = `/logout`
    })
    $('#send').on('click', function () {
        $.ajax({
            type: "GET",
            url: `/comment?live_id=${live_id}&text=${$('#comment').val()}`,
            contentType: "application/json",
            dataType: "json"
        }).done(function (res) {
            $('#comment').val('')
        })
    })
    $('#join').on('click', function () {
        $.ajax({
            type: "GET",
            url: `/join?live_id=${live_id}`,
            contentType: "application/json",
            dataType: "json"
        })
    })
})