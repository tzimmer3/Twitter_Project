import smtplib

# Configure server
server = smtplib.SMTP('smtp.gmail.com', 587)

# Start server
server.startls()

# Login: Username, Password
server.login('tzimme9@gmail.com', '32Woodlawn')

# Send email
server.sendmail('tzimme9@gmail.com', 'tzimme9@gmail.com', 'Mail sent from python script.')

# Print result
print('Mail Sent')