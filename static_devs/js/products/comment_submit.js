const recommentSubmit = (pk) => {
    const textBox = document.querySelectorAll('.recomment-input-box');
    const targetComment = [...textBox].find(
        (elem) => parseInt(elem.getAttribute('name')) === pk
    );

    $.ajax({
        type: 'POST',
        url: `/comment/product/${productPK}/comment/${pk}/recomment/`,
        dataType: 'json',
        data: {
            text: targetComment.value,
            csrfmiddlewaretoken: csrftoken,
        },

        success: function (data) {
            const comment = `
            <div class="recomment relative" name="${data.pk}">
                    <div class="flex items-center recomment-info">
                        <div class="recomment-arrow"></div>
                        <div class="recomment-author flex items-center">
                            <img src="${data.profile_image}" class="comment-author--profile-image">
                            <div class="comment-author--id">${data.author}</div>
                        </div>
                        <div class="bar"></div>
                        <div class="comment-create text-center recomment-create">
                            ${data.create_at}
                        </div>
                        <div class="bar"></div>
                        <div class="recomment-report flex items-center ml-auto">
                            <img src="${reportButtonImageURL}"
                                alt="">
                            <div class="comment-report--report button">신고하기</div>
                        </div>
                    </div>
                    <div class="absolute recomment-like-button-wrap button">
                        <div class="recomment-like-button relative"
                            style="background-image: url(${recommentLikeButtonImageURL});">
                            <p class="recomment-like-count absolute text-center align-text-bottom">0</p>
                        </div>
                    </div>
                    <div class="recomment-content">
                        <div class="recomment-text">
                            <div class="recomment-text--text">${data.text}</div>
                            <div class="recomment-text-options-wrap flex justify-between">
                                <div></div>
                                <div class="recomment-text-options flex">
                                    <div class="recomment-text-options--edit button comment-text-options--edit"  onclick="RecommentEdit(this, ${data.pk})">수정</div>
                                    <div class="recomment-text-options--delete button comment-text-options--delete" onclick="RecommentDelete(${data.pk})">삭제</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="horizon-bar mx-auto"></div>
            `;

            targetComment.parentNode.parentNode.insertAdjacentHTML(
                'beforeend',
                comment
            );
            targetComment.value = '';

            const t = document
                .querySelector(
                    `div[class="recomment relative"][name="${data.pk}"] .recomment-like-button-wrap`
                )
                .addEventListener('click', (e) => recommentLike(e));

            shootToastMessage('답글이 등록되었습니다.');
        },
    });
};
