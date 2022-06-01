from django.test import TestCase

#test all the models
from Menus.models import Menu, build_menu


class DeleteMenuItemBugTestCase( TestCase ):
    fixtures = [ 'menu_bug.json' ]

    def test_delete_menuitem(self):
        # First get the menu
        menu = Menu.objects.get( name__exact='Main menu' )
        menuroot = menu.menuitem_set.filter( level__exact=0 )[0]
        menuitems = menuroot.get_descendants()

        # Ensure we have a proper MPTT tree first
        self.assertEqual( len( menuitems ), 4 )
        self.assertEqual( menuroot.lft, 1 )
        self.assertEqual( menuroot.rght, 10 )
        self.assertEqual( menuitems[0].lft, 2 )
        self.assertEqual( menuitems[0].rght, 7 )
        self.assertEqual( menuitems[1].lft, 3 )
        self.assertEqual( menuitems[1].rght, 6 )
        self.assertEqual( menuitems[2].lft, 4 )
        self.assertEqual( menuitems[2].rght, 5 )
        self.assertEqual( menuitems[3].lft, 8 )
        self.assertEqual( menuitems[3].rght, 9 )

        # Delete the item
        menuitems[1].delete()

        # Verify the new tree
        menu = Menu.objects.get( name__exact='Main menu' )
        menuroot = menu.menuitem_set.filter( level__exact=0 )[0]
        menuitems = menuroot.get_descendants()

        self.assertEqual( len( menuitems ), 2 )
        self.assertEqual( menuroot.lft, 1 )
        self.assertEqual( menuroot.rght, 6 )
        self.assertEqual( menuitems[0].lft, 2 )
        self.assertEqual( menuitems[0].rght, 3 )
        self.assertEqual( menuitems[1].lft, 4 )
        self.assertEqual( menuitems[1].rght, 5 )


class RecursionBugTestCase( TestCase ):
    fixtures = [ 'recursion_bug.json' ]

    def test_build_menu( self ):
        """
        Testing a bug where the urls.sort() method in the end of build_menu
        reached maximum recursion depth when comparing list elements. Each list
        element is a two-tuple, where we actually only want to sort on the first
        element in the tuple (the URL), but where sorting on both elements.
        """
        build_menu( 'Main menu' )
