const data=JSON.parse(document.getElementById('quiz-data').textContent);
const results=new Map(),root=document.getElementById('questions'),labels='ABCDEF';
const subject=document.getElementById('subject'),questionType=document.getElementById('question-type'),hideCorrect=document.getElementById('hide-correct');
function filterQuestions(){let count=0;for(const card of root.children){const show=(!subject.value||card.dataset.subject===subject.value)&&(!questionType.value||card.dataset.type===questionType.value)&&(!hideCorrect.checked||results.get(Number(card.dataset.id))!==true);card.hidden=!show;if(show)count++;}document.getElementById('visible-count').textContent=`当前显示 ${count} / ${data.length} 题`;document.getElementById('quiz-empty').hidden=count!==0;}
function answerLabel(q,text){return labels[q.options.indexOf(text)]+'. '+text;}
for(const q of data){
 const card=document.createElement('article');card.className='question';card.dataset.subject=q.subject;card.dataset.type=q.type;card.dataset.id=String(q.id);
 const meta=document.createElement('div');meta.className='qmeta';meta.textContent=String(q.id)+' · '+q.subject+' · '+q.type+' · '+q.difficulty;card.append(meta);
 const fs=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent=q.stem;fs.append(legend);
 q.options.forEach((option,index)=>{const label=document.createElement('label');label.className='option';const input=document.createElement('input');input.type=q.type==='多选'?'checkbox':'radio';input.name='question-'+q.id;input.value=String(index);const span=document.createElement('span');span.textContent=labels[index]+'. '+option;label.append(input,span);fs.append(label);});
 const button=document.createElement('button');button.type='button';button.textContent='确认作答，查看解析';button.disabled=true;
 const feedback=document.createElement('div');feedback.className='feedback';feedback.hidden=true;feedback.setAttribute('aria-live','polite');
 fs.addEventListener('change',()=>{button.disabled=!fs.querySelector('input:checked');feedback.hidden=true;});
 button.addEventListener('click',()=>{
  const chosen=[...fs.querySelectorAll('input:checked')].map(input=>q.options[Number(input.value)]);
  const missed=q.answer.filter(answer=>!chosen.includes(answer)),wrong=chosen.filter(answer=>!q.answer.includes(answer));
  const good=missed.length===0&&wrong.length===0;results.set(q.id,good);feedback.className='feedback'+(good?'':' wrong');feedback.replaceChildren();
  const title=document.createElement('strong');title.textContent=good?'回答正确':'这题需要再巩固';feedback.append(title);
  if(!good){const differences=document.createElement('p');differences.className='selection-error';differences.textContent='漏选：'+(missed.map(text=>answerLabel(q,text)).join('；')||'无')+'。误选：'+(wrong.map(text=>answerLabel(q,text)).join('；')||'无')+'。';feedback.append(differences);}
  for(const text of ['正确答案：'+q.answer.map(answer=>answerLabel(q,answer)).join('；'),'解析：'+q.explanation,'知识点：'+q.knowledge_point,'依据：'+q.source]){const paragraph=document.createElement('p');paragraph.textContent=text;feedback.append(paragraph);}
  feedback.hidden=false;button.textContent='重新核对答案';document.getElementById('progress').textContent=`本页已答 ${results.size} / ${data.length}，答对 ${[...results.values()].filter(Boolean).length} 题`;filterQuestions();
 });
 card.append(fs,button,feedback);root.append(card);
}
for(const control of [subject,questionType,hideCorrect])control.addEventListener('change',filterQuestions);filterQuestions();