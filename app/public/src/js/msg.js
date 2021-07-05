window.msg = function (data={status: 'info', msg: 'Something wrong happened?!'}, auto_remove=true) {
	if (!data || !data.msg)
		return;

    if (data.status == 'fail') {
        data.status = 'danger';
        var icon_name = 'times';
    } else if (data.status == 'success')
		var icon_name = 'check';
    else if (data.status == 'warning')
		var icon_name = 'exclamation'
    else
        var icon_name = 'info';

    select('#msgs-container').insertAdjacentHTML('afterbegin', `
		<div class="alert alert-${data.status} alert-dismissible fade show msg" role="alert">
            <i class="fas fa-${icon_name} msg-icon"></i>${data.msg}
			<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
		</div>
    `);

    if (auto_remove) {
        setTimeout(() => {
			(new Alert(select('.msg'))).close();
        }, 10000);
    }
};
