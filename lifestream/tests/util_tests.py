#!/usr/bin/env python
#:coding=utf-8:

from base import *

from lifestream.util import * 

class TagStrippingTest(HTMLSanitizationTest):
    test_html = (
        (
            u'<b>This is a test</b>', 
            u'<b>This is a test</b>',
        ),
        (
            u'<script type="text/javascript">alert("DANGER!!");</script> Will Robinson',
            u'alert(&quot;DANGER!!&quot;); Will Robinson',
        ),
        (
            u'<a href="http://www.ianlewis.org/" rel="me" onclick="alert(\'woah!!\')">This is a test</a>',
            u'<a href="http://www.ianlewis.org/" rel="me">This is a test</a>',
        ),
        (
            u'<CRazY>Crazy Text</crazy>',
            u'Crazy Text',
        )
    )

class EntitiesTest(HTMLSanitizationTest):
    test_html = (
        (
            u'<b>Ian\'s Homepage</b>', 
            u'<b>Ian&apos;s Homepage</b>',
        ),
        (
            u'"I CaN HaZ SoMe < TeXt?"',
            u'&quot;I CaN HaZ SoMe &lt; TeXt?&quot;',
        ),
        (
            u'"I CaN HaZ SoMe <TeXt>?"',
            u'&quot;I CaN HaZ SoMe ?&quot;',
        ),
        (
            u'Ice Cream & &quot;Chocolate&quot;',
            u'Ice Cream &amp; &quot;Chocolate&quot;',
        )
    )

class CSSSanitizationTest(HTMLSanitizationTest):
    valid_tags = {
        'div': ('style',),
        'span': ('style',),
    }
    valid_styles = (
        "color",
        "font-weight",
    )
    test_html = (
        (
            u'<span style="color:#FFF;position:absolute;">My Homepage</span>', 
            u'<span style="color:#FFF;">My Homepage</span>', 
        ),
        (
            u'<span style="color:#FFF;position:absolute;font-weight:bold;">My Homepage</span>', 
            u'<span style="color:#FFF;font-weight:bold;">My Homepage</span>', 
        ),
        (
            u'<span style="color:#FFF;position:absolute   ">My Homepage</span>', 
            u'<span style="color:#FFF;">My Homepage</span>', 
        ),
        (
            u'<span style="  color:#FFF;  position:absolute;\tfont-weight:bold  ">My Homepage</span>', 
            u'<span style="color:#FFF;font-weight:bold;">My Homepage</span>', 
        ),
        (
            u'<span style="  color:#FFF;  position:absolute;\tfont-weight:bold;  aaaaa">My Homepage</span>', 
            u'<span style="color:#FFF;font-weight:bold;">My Homepage</span>', 
        ),
    )

class EntityTest(EntityConversionTest):
    test_html = (
        (
            u'&quot;Ian&apos;s Homepage&quot;',
            u'"Ian\'s Homepage"',
        ),
        (
            u'&lt;Ian&apos;s Homepage&gt;',
            u'<Ian\'s Homepage>',
        ),
        (
            u'"Ian\'s Homepage"',
            u'"Ian\'s Homepage"',
        ),
    )
