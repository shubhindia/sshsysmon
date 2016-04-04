from os import path
import json
import logging
import pybars

TEMPLATE_PATH = path.dirname(path.realpath(__file__))


# Controlling methods for template building
def __ifEq(this, options, left, right):
	print left, right
	if left == right:
		return options['fn'](this)
	else:
		return options['inverse'](this)

__helpers = {
	'ifEq' : __ifEq
}

def __template(src, data):
	hbCompiler = pybars.Compiler()
	hbTemplate = hbCompiler.compile(unicode(src))
	return hbTemplate(data, helpers = __helpers)

def template(name, data):
	if name:
		tplPath = path.join(TEMPLATE_PATH, name + ".hb")
		if path.isfile(tplPath):
			logging.debug("Building template with: " + tplPath)
			return __template(open(tplPath, 'r').read(), data)
		else:
			logging.error("Unable to find requested template: " + name)

	return json.dumps(data)