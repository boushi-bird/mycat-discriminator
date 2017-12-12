require('whatwg-fetch');

const uploadFileReader = new FileReader();
const selectFile = (file) => {
  if (!file) {
    showResult('画像を選択して下さい');
    return;
  }
  showResult('判別中...');
  uploadFileReader.readAsDataURL(file);
  uploadFileReader.onload = () => {
    preview.setAttribute('src', uploadFileReader.result);
  };
  const body = new FormData();
  body.append('upload', file)
  fetch('/api/upload', {
    method: 'POST',
    body,
  }).then(response => {
    response.json().then(json => {
      showResult(createAnswerText(json));
    });
  }).catch(e => {
    showResult('判別に失敗しました。');
    console.error(e);
  });
};
const createAnswerText = (json) => {
  const { answer, all_ratios } = json;
  if (!answer) {
    return '判別に失敗しました。';
  }
  let all = '';
  all_ratios.forEach(r => {
    all = `${all}${r.label}: ${r.ratio}%<br />`;
  });
  let mainMessage;
  if (answer.ratio > 95) {
    mainMessage = `${answer.label}です`;
  } else if (answer.ratio > 70) {
    mainMessage = `多分${answer.label}です`;
  } else {
    mainMessage = `${answer.label}かもしれません`;
  }
  return `${mainMessage}<br />${all}`;
};
const showResult = (result_text) => {
  const result = document.getElementById('result');
  result.innerHTML = result_text;
};

document.addEventListener('DOMContentLoaded', () => {
  selectFile(null);
  const upload = document.getElementById('upload');
  const preview = document.getElementById('preview');
  document.addEventListener('change', (e) => {
    preview.removeAttribute('src');
    selectFile(e.target.files[0]);
  });
});
