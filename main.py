import discord
import urllib.request
import random
import os
import json
import shutil
import chanrestrict

LATEX_TEMPLATE="template.tex"

HELP_MESSAGE = r"""
Hello! I'm the *HeXit* mathematics bot!

You can type mathematical *LaTeX* into the chat and I'll automatically render it!
Simply use the `!tex` command.

**Examples**
`!tex x = 7`
`!tex \sqrt{a^2 + b^2} = c`
`!tex \int_0^{2\pi} \sin{(4\theta)} \mathrm{d}\theta`

**Notes**
Using the `\begin` or `\end` in the *LaTeX* will probably result in something failing.

"""

class LatexBot(discord.Client):
	def __init__(self):
		intents = discord.Intents.default()
		intents.message_content = True
		super().__init__(intents=intents)

		self.check_for_config()
		self.settings = json.loads(open('settings.json').read())

		if 'latex' not in self.settings:
			self.settings['latex'] = {
						'background-colour': '36393E',
						'text-colour': 'DBDBDB',
						'dpi': '200'
				}

		chanrestrict.setup(self.settings['channels']['whitelist'],
							self.settings['channels']['blacklist'])

	def check_for_config(self):
		if not os.path.isfile('settings.json'):
			shutil.copyfile('settings_default.json', 'settings.json')
			print('Now you can go and edit `settings.json`.')
			print('See README.md for more information on these settings.')

	def vprint(self, *args, **kwargs):
		if self.settings.get('verbose', False):
			print(*args, **kwargs)

	async def on_ready(self):
		print('HeXit (1079154383117365358) is now online!')

	async def on_message(self, message):
		if chanrestrict.check(message):
			msg = message.content
			print('Processing', msg)

			for c in self.settings['commands']['render']:
				if msg.startswith(c):
					latex = msg[len(c):].strip()
					self.vprint('Latex:', latex)

					num = str(random.randint(0, 2 ** 31))
					if self.settings['renderer'] == 'external':
						fn = self.generate_image_online(latex)
					if self.settings['renderer'] == 'local':
						fn = self.generate_image(latex, num)
						# raise Exception('TODO: Renable local generation')

					if fn and os.path.getsize(fn) > 0:
						await message.channel.send(file=discord.File(fn))
						self.cleanup_output_files(num)
						self.vprint('Success!')
					else:
						await message.channel.send('Something broke. Check the syntax of your message. :frowning:')
						self.cleanup_output_files(num)
						self.vprint('Failure.')

					break

			if msg in self.settings['commands']['help']:
				self.vprint('Showing help')
				await message.author.send(HELP_MESSAGE)

	def generate_image(self, latex, name):

		latex_file = name + '.tex'
		dvi_file = name + '.dvi'
		png_file = name + '1.png'

		with open(LATEX_TEMPLATE, 'r') as textemplatefile:
			textemplate = textemplatefile.read()

			with open(latex_file, 'w') as tex:
				backgroundcolour = self.settings['latex']['background-colour']
				textcolour = self.settings['latex']['text-colour']
				latex = textemplate.replace('__DATA__', latex).replace('__BGCOLOUR__', backgroundcolour).replace('__TEXTCOLOUR__', textcolour)

				tex.write(latex)
				tex.flush()
				tex.close()

		imagedpi = self.settings['latex']['dpi']
		latexsuccess = os.system('latex -quiet -interaction=nonstopmode ' + latex_file)
		if latexsuccess == 0:
			os.system('dvipng -q* -D {0} -T tight '.format(imagedpi) + dvi_file)
			return png_file
		else:
			return ''

	def generate_image_online(self, latex):
		url = 'http://frog.isima.fr/cgi-bin/bruno/tex2png--10.cgi?'
		url += urllib.parse.quote(latex, safe='')
		fn = str(random.randint(0, 2 ** 31)) + '.png'
		urllib.request.urlretrieve(url, fn)
		return fn

	def cleanup_output_files(self, outputnum):
		try:
			os.remove(outputnum + '.tex')
			os.remove(outputnum + '.dvi')
			os.remove(outputnum + '.aux')
			os.remove(outputnum + '.log')
			os.remove(outputnum + '1.png')
		except OSError:
			pass

if __name__ == "__main__":
	bot = LatexBot()
	if bot.settings['login_method'] != 'token':
		raise Exception('Bad config: "login_method" should set to "token"')
	bot.run(bot.settings['login']['token'])
