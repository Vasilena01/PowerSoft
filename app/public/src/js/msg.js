window.msg = (data={status: 'info', msg: 'Something wrong happened?!'}, auto_remove=true) => {
	if (!data || !data.msg)
		return

    select('#msgs-container').insertAdjacentHTML('afterbegin', `
		<div class="msg msg-${data.status}">
			<span>${data.msg}</span>
			<button type="button" class="btn-close" onclick="dismiss_msg(this.parentElement)" aria-label="Затвори"></button>
		</div>
    `)

    if (auto_remove) {
        setTimeout(() => {
			dismiss_msg(select('.msg'))
        }, 10000)
    }
}

window.dismiss_msg = (msg) => {
	msg.remove()
}
