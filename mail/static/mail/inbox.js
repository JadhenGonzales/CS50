document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // Other functions
  document.querySelector('#compose-form').onsubmit = send_email;
  document.querySelector('#email-archive').addEventListener('click', function() {archive(this.value);});
  document.querySelector('#email-unarchive').addEventListener('click', function() {unarchive(this.value);});
  document.querySelector('#email-reply').addEventListener('click', function() {reply(this.value);});

  // By default, load the inbox
  load_mailbox('inbox');
});


function add_to_mailbox(emails) {
  const container = document.querySelector('#mailbox-container')

  emails.forEach(email => {
    const element = document.createElement('div');
    element.innerHTML = generate_mailbox_HTML(email);
    element.addEventListener('click', () => view_email(email.id));

    if (email.read === true) {
      element.classList.add('bg-dark-subtle')
    }

    container.append(element);
  });
}


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function generate_mailbox_HTML(email) {
  return `
    <div class="border border-black p-1">
      <div>from: ${email.sender}</div>
      <div>${email.subject}</div>
      <div>${email.timestamp}</div>
    </div>
  `
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name and clear contents
  document.querySelector('#mailbox-header').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#mailbox-container').innerHTML = ''

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // To do show emails
      add_to_mailbox(emails);
  });

}


function send_email() {

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
  
  return false;
}


function view_email(email_id) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      
      // Populate HTML with email contents
      document.querySelector('#email-body').innerHTML = email.body;
      document.querySelector('#email-sender').innerHTML = email.sender;
      document.querySelector('#email-subject').innerHTML = email.subject;
      document.querySelector('#email-timestamp').innerHTML = email.timestamp;
      show_buttons(email);

      return email;
  })
  .then(email => {
    // Mark email as read
    return fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
  })
  .catch(error => {
    console.log('Error:', error);
  });
}


function archive(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  .then(result => {
    load_mailbox('inbox');
    return result;
  })
  .catch(error => {
    console.log('Error:', error);
  });
}


function unarchive(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(result => {
    load_mailbox('inbox');
    return result;
  })
  .catch(error => {
    console.log('Error:', error);
  });
}


function reply(email_id) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Get previous email details
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Fill out fields
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-body').value = `
      On ${email.timestamp} ${email.sender} wrote: ${email.body}
    `;
    
   if (email.subject.slice(0, 4) == "Re: ") {
    document.querySelector('#compose-subject').value = email.subject;
   } else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
   }
  })
  .catch(error => {
    console.log('Error:', error);
  });
}


function show_buttons(email) {
  user = document.querySelector('#user-header').innerHTML

  if (email.sender != user) {
    document.querySelector('#email-reply').style.display = 'block';
    document.querySelector('#email-reply').value = email.id;
    // Buttons for archive and unarchive
    if (email.archived === false) {
      document.querySelector('#email-archive').style.display = 'block';
      document.querySelector('#email-unarchive').style.display = 'none';

      document.querySelector('#email-archive').value = email.id;
    } else {
      document.querySelector('#email-unarchive').style.display = 'block';
      document.querySelector('#email-archive').style.display = 'none';

      document.querySelector('#email-unarchive').value = email.id;
    }
  } else {
    document.querySelector('#email-archive').style.display = 'none';
    document.querySelector('#email-unarchive').style.display = 'none';
    document.querySelector('#email-reply').style.display = 'none';
  }
}