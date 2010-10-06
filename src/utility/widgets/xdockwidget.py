# Ported from KoDockWidgetTitleBar.cpp which is part of KOffice
# Copyright (c) 2007 Marijn Kruisselbrink <m.kruisselbrink@student.tue.nl>
# Copyright (C) 2007 Thomas Zander <zander@kde.org>
# The code is distributed under GPL 2 or any later version


from PyQt4.QtCore import Qt, QSize, QPoint, QRect, pyqtSlot, \
pyqtSignal
from PyQt4.QtGui import QAbstractButton, QStyleOptionToolButton, QStyle, QPainter, \
QWidget, QIcon, QStylePainter, QDockWidget, QStyleOptionDockWidgetV2, QHBoxLayout




def hasFeature( dockwidget, feature ):
    return dockwidget.features() & feature == feature



class XDockWidgetTitleBarButton( QAbstractButton ):


    def __init__( self, titlebar ):
        QAbstractButton.__init__( self, titlebar )
        self.setFocusPolicy( Qt.NoFocus )

    def sizeHint( self ):
        self.ensurePolished()
        margin = self.style().pixelMetric( QStyle.PM_DockWidgetTitleBarButtonMargin, None, self )
        if self.icon().isNull():
            return QSize( margin, margin )
        iconSize = self.style().pixelMetric( QStyle.PM_SmallIconSize, None, self )
        pm = self.icon().pixmap( iconSize )
        return QSize( pm.width() + margin, pm.height() + margin )


    def enterEvent( self, event ):
        if self.isEnabled():
            self.update()
        QAbstractButton.enterEvent( self, event )


    def leaveEvent( self, event ):
        if self.isEnabled():
            self.update()
        QAbstractButton.leaveEvent( self, event )


    def paintEvent( self, _event ):
        p = QPainter( self )
#        r = self.rect()
        opt = QStyleOptionToolButton()
        opt.init( self )
        opt.state |= QStyle.State_AutoRaise
        if self.isEnabled() and self.underMouse() and \
           not self.isChecked() and not self.isDown():
            opt.state |= QStyle.State_Raised
        if self.isChecked():
            opt.state |= QStyle.State_On
        if self.isDown():
            opt.state |= QStyle.State_Sunken
        self.style().drawPrimitive( 
            QStyle.PE_PanelButtonTool, opt, p, self )
        opt.icon = self.icon()
        opt.subControls = QStyle.SubControls()
        opt.activeSubControls = QStyle.SubControls()
        opt.features = QStyleOptionToolButton.None
        opt.arrowType = Qt.NoArrow
        size = self.style().pixelMetric( QStyle.PM_SmallIconSize, None, self )
        opt.iconSize = QSize( size, size )
        self.style().drawComplexControl( QStyle.CC_ToolButton, opt, p, self )


import os
__icon_path__ = os.path.dirname( os.path.abspath( __file__ ) )

class XDockWidgetTitleBar( QWidget ):


    def __init__( self, dockWidget ):
        super( XDockWidgetTitleBar, self ).__init__( dockWidget )
        self.openIcon = QIcon( ":/icons/res/arrow-down.png" )
        self.closeIcon = QIcon( ":/icons/res/arrow-right.png" )
        q = dockWidget
        self.floatButton = XDockWidgetTitleBarButton( self )
        self.floatButton.setIcon( q.style().standardIcon( 
            QStyle.SP_TitleBarNormalButton, None, q ) )
        self.floatButton.clicked.connect( self.toggleFloating )
        self.floatButton.setVisible( True )
        self.closeButton = XDockWidgetTitleBarButton( self )
        self.closeButton.setIcon( q.style().standardIcon( 
            QStyle.SP_TitleBarCloseButton, None, q ) )
        self.closeButton.clicked.connect( dockWidget.close )
        self.closeButton.setVisible( True )
        self.collapseButton = XDockWidgetTitleBarButton( self )
        self.collapseButton.setIcon( self.openIcon )
        self.collapseButton.clicked.connect( self.toggleCollapsed )
        self.collapseButton.setVisible( True )

        dockWidget.featuresChanged.connect( self.featuresChanged )
        self.featuresChanged( 0 )


    def minimumSizeHint( self ):
        return self.sizeHint()


    def sizeHint( self ):
        q = self.parentWidget()
        mw = q.style().pixelMetric( QStyle.PM_DockWidgetTitleMargin, None, q )
        fw = q.style().pixelMetric( QStyle.PM_DockWidgetFrameWidth, None, q )
        closeSize = QSize( 0, 0 )
        if self.closeButton:
            closeSize = self.closeButton.sizeHint()
        floatSize = QSize( 0, 0 )
        if self.floatButton:
            floatSize = self.floatButton.sizeHint()
        hideSize = QSize( 0, 0 )
        if self.collapseButton:
            hideSize = self.collapseButton.sizeHint()
        buttonHeight = max( max( closeSize.height(), floatSize.height() ),
                            hideSize.height() ) + 2
        buttonWidth = closeSize.width() + floatSize.width() + hideSize.width()
        titleFontMetrics = q.fontMetrics()
        fontHeight = titleFontMetrics.lineSpacing() + 2 * mw
        height = max( buttonHeight, fontHeight )
        return QSize( buttonWidth + height + 4 * mw + 2 * fw, height )


    def paintEvent( self, _event ):
        p = QStylePainter( self )
        q = self.parentWidget()
        fw = q.isFloating() and q.style().pixelMetric( 
            QStyle.PM_DockWidgetFrameWidth, None, q ) or 0
        mw = q.style().pixelMetric( QStyle.PM_DockWidgetTitleMargin, None, q )
        titleOpt = QStyleOptionDockWidgetV2()
        titleOpt.initFrom( q )
        titleOpt.rect = QRect( 
            QPoint( fw + mw + self.collapseButton.size().width(), fw ),
            QSize( 
               self.geometry().width() - ( fw * 2 ) - \
               mw - self.collapseButton.size().width(),
               self.geometry().height() - ( fw * 2 ) ) )
        titleOpt.title = q.windowTitle()
        titleOpt.closable = hasFeature( q, QDockWidget.DockWidgetClosable )
        titleOpt.floatable = hasFeature( q, QDockWidget.DockWidgetFloatable )
        p.drawControl( QStyle.CE_DockWidgetTitle, titleOpt )


    def resizeEvent( self, _event ):
        q = self.parentWidget()
        fw = q.isFloating() and q.style().pixelMetric( 
            QStyle.PM_DockWidgetFrameWidth, None, q ) or 0
        opt = QStyleOptionDockWidgetV2()
        opt.initFrom( q )
        opt.rect = QRect( 
            QPoint( fw, fw ),
            QSize( 
              self.geometry().width() - ( fw * 2 ),
              self.geometry().height() - ( fw * 2 ) ) )
        opt.title = q.windowTitle()
        opt.closable = hasFeature( q, QDockWidget.DockWidgetClosable )
        opt.floatable = hasFeature( q, QDockWidget.DockWidgetFloatable )

        floatRect = q.style().subElementRect( 
            QStyle.SE_DockWidgetFloatButton, opt, q )
        if not floatRect.isNull():
            self.floatButton.setGeometry( floatRect )
        closeRect = q.style().subElementRect( 
        QStyle.SE_DockWidgetCloseButton, opt, q )
        if not closeRect.isNull():
            self.closeButton.setGeometry( closeRect )
        top = fw
        if not floatRect.isNull():
            top = floatRect.y()
        elif not closeRect.isNull():
            top = closeRect.y()
        size = self.collapseButton.size()
        if not closeRect.isNull():
            size = self.closeButton.size()
        elif not floatRect.isNull():
            size = self.floatButton.size()
        collapseRect = QRect( QPoint( fw, top ), size )
        self.collapseButton.setGeometry( collapseRect )


    def setCollapsed( self, collapsed ):
        q = self.parentWidget()
        if q and q.widget() and q.widget().isHidden() != collapsed:
            self.toggleCollapsed()


    def toggleFloating( self ):
        q = self.parentWidget()
        q.setFloating( not q.isFloating() )


    def toggleCollapsed( self ):
        q = self.parentWidget()
        if not q:
            return
        #q.widget().setVisible(q.widget().isHidden())
        #self.collapseButton.setIcon(q.widget().isHidden() and self.closeIcon or self.openIcon)
        q.toggleCollapsed()
        self.collapseButton.setIcon( q.collapsed and self.openIcon or self.closeIcon )


    def featuresChanged( self, _features ):
        q = self.parentWidget()
        self.closeButton.setVisible( hasFeature( q, QDockWidget.DockWidgetClosable ) )
        self.floatButton.setVisible( hasFeature( q, QDockWidget.DockWidgetFloatable ) )
        #self.resizeEvent(None)



class XDockMainWidgetWrapper( QWidget ):


    def __init__( self, dockwidget ):
        QWidget.__init__( self, dockwidget )
        self.widget = None
        self.widget_height = 0
        self.hlayout = QHBoxLayout( self )
        self.setLayout( self.hlayout )


    def setWidget( self, widget ):
        self.widget = widget
        self.widget_height = widget.height()
        self.layout().addWidget( widget )


    def isCollapsed( self ):
        return self.widget.isVisible()


    def setCollapsed( self, flag ):
        if flag:
            self.widget_height = self.widget.height()
            self.setFixedHeight( 0 )
            self.widget.setVisible( False )
        else:
            self.setFixedHeight( self.widget_height )
            self.widget.setVisible( True )
            self.setMinimumHeight( 0 )
            self.setMaximumHeight( 2048 )


    def sizeHint( self ):
        if self.widget:
            return self.widget.sizeHint()
        else:
            return QWidget.sizeHint( self )



class XDockWidget( QDockWidget ):

    stateChanged = pyqtSignal( bool )

    def __init__( self, *args ):
        super( XDockWidget, self ).__init__( *args )
        self.titleBar = XDockWidgetTitleBar( self )
        self.setTitleBarWidget( self.titleBar )
        self.mainWidget = None

        self.topLevelChanged[bool].connect( self.changeStatus )

    def changeStatus( self, status ):
        if status == True:
            self.collapsed = False

    def setWidget( self, widget ):
        self.mainWidget = XDockMainWidgetWrapper( self )
        self.mainWidget.setWidget( widget )
        QDockWidget.setWidget( self, self.mainWidget )

    @pyqtSlot( bool )
    def setCollapsed( self, flag ):
        self.mainWidget.setCollapsed( flag )
        self.stateChanged.emit( flag )


    def collapsed( self ):
        return self.mainWidget.isCollapsed()

    collapsed = property( collapsed, setCollapsed )

    def toggleCollapsed( self ):
        self.setCollapsed( self.collapsed )
        self.stateChanged.emit( self.collapsed )



if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit
    app = QApplication( sys.argv )
    win = QMainWindow()
    dock1 = XDockWidget( "1st dockwidget", win )
    dock1.setFeatures( QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable )
    combo = QComboBox( dock1 )
    dock1.setWidget( combo )
    win.addDockWidget( Qt.LeftDockWidgetArea, dock1 )
    dock2 = XDockWidget( "2nd dockwidget" )
    button = QPushButton( "Hello, world!", dock2 )
    dock2.setWidget( button )
    win.addDockWidget( Qt.RightDockWidgetArea, dock2 )
    edit = QTextEdit( win )
    win.setCentralWidget( edit )
    win.resize( 640, 480 )
    win.show()
    app.exec_()
