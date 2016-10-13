# pylint: disable=unused-variable


from verchew import utils


def describe_display():

    def it_shows_text():
        utils.display("foobar")
