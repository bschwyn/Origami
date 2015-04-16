# Origami
optimization algorithms to find origami crease patterns / origami design aid

This program is based on the theory and mathematics developed in Origami Design Secrets: Mathematical 
Methods for an Ancient Art by Robert J. Lang.

Background
Origami is the art of folding paper (usually squares)into sculptures, without cuts. Most origami is
sculptures of animals or everyday objects, out of one or two pieces of paper. The finished sculptures
(models) are angular, more-or-less abstract representations of the intended subject. There are other
types of origami, such as modular origami, where small folded subunits are assembled into regular
geometric structures, and action origami with moving parts, but for this program we are interested in
more standard, scupltural models.

An origami sculpture is folded from an *origami base*. An origami base is a configuration of the
paper which has the rough geometric structure of the final form, without any aesthetic shaping.
For example http://www.wikihow.com/Make-an-Origami-Bird-Base is the base for the traditional crane
model seen here: http://commons.wikimedia.org/wiki/File:Origami-crane.jpg. A base has all of the 
flaps (long sections of paper with hinges) connected in same way the different appendages are 
connected - the different flaps then get transformed into their respective parts of the finished
model. The bird base has four flaps of equal length connected at one vertex, these then get shaped
into the 2 wings, head and tail of the crane.

This Program
Given a stick figure representation of a subject, this program calculates the locations of major
crease intersections such that the paper is used most effiently. There a many ways to fold a crane
(or in this case to create an origami base with 4 equal-length, centrally-hinged flaps) however, the
one which largest ratio of flap length to the size of the paper results in the largest possible crane.
For this model, the bird base is most efficient.

Tutorial
