export const formHandler = () => {
  const form = document.querySelector('#question-form')
  const errorBlock = document.querySelector('.form__error')
  const btn = document.querySelector('.form__btn')
  const answerContainer = document.querySelector('.answer__chat')

  initChat(answerContainer)

  const params = new URLSearchParams(window.location.search)
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault()

      const input = form.querySelector('.form__input')
      const url = params.get('url')

      if (!url) {
        ; (errorBlock as HTMLElement).innerText = 'No article url passed'
        errorBlock?.classList.add('form__error--active')
        return
      }

      if (isValid(input as HTMLInputElement)) {
        const ctx = localStorage.getItem('j-ml-ctx') || ''

        sendAndHandleAnswer(
          btn as HTMLButtonElement,
          answerContainer as HTMLElement,
          errorBlock as HTMLElement,
          {
            article: { link: url },
            context: ctx,
            query_text: (input as HTMLInputElement).value,
            instruction: '',
          }
        )
          ; (input as HTMLInputElement).value = ''
      } else {
        ; (errorBlock as HTMLElement).innerText = 'Field have to be filled'
        errorBlock?.classList.add('form__error--active')
        return
      }
    })
  }
}

const isValid = (input: HTMLInputElement): boolean => {
  if (!input) return false

  return !!input.value && !!input.value.trim()
}

const sendAndHandleAnswer = async (
  btn: HTMLButtonElement,
  answerContainer: HTMLElement,
  errorBlock: HTMLElement,
  options: {
    article: { link: string }
    context: string
    query_text: string
    instruction: string
  }
) => {
  errorBlock.innerText = ''
  errorBlock.classList.remove('form__error--active')
  btn.innerHTML = 'Loading...'

  const question = createChatElem(options.query_text, 'question')

  answerContainer.appendChild(question)

  try {
    const result = await fetch(
      'https://dizyme.aicidlab.itmo.ru/a6d370833a02f53db6a0a30800704994/',
      {
        method: 'POST',
        body: JSON.stringify(options),
        headers: {
          'Content-type': 'application/json',
        },
      }
    )
    const json = await result.json()

    if (json?.msg) {
      errorBlock.innerHTML = json.msg
      throw new Error(json.msg)
    }

    let answer

    if (json?.answer) {
      answer = createChatElem(json.answer, 'answer__text')
      localStorage.setItem('j-ml-ctx', json.context)
    } else {
      answer = createChatElem(
        'There is some error appear, please try again',
        'answer__text'
      )
    }

    answerContainer.appendChild(answer)
  } catch (err) {
    console.error(err)
  } finally {
    btn.innerHTML = 'Ask'
  }
}

const createChatElem = (text: string, className: string): HTMLElement => {
  const el = document.createElement('div')
  el.classList.add(className)

  el.innerHTML = `<p>${text}</p>`

  return el
}

const initChat = (container: Element | null) => {
  const ctx = localStorage.getItem('j-ml-ctx')

  if (!ctx) return

  let chat: { question: string; answer: string }[] = []

  ctx
    .split('\n')
    ?.filter((item) => !!item)
    ?.map((item, index, arr) => {
      if (item.startsWith('response')) return

      chat.push({
        question: item,
        answer: arr[index + 1].replace('response: ', ''),
      })
    })

  if (chat.length > 0 && container) {
    chat.map((item) => {
      const questionEl = createChatElem(item.question, 'question')
      const answerEl = createChatElem(item.answer, 'answer__text')

      container.appendChild(questionEl)
      container.appendChild(answerEl)
    })
  }
}
