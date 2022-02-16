<template>
  <v-container>
    <v-card
      elevation="12"
      width="256"
    >
      <v-navigation-drawer
        v-model="menu"
        clipped
        app
        :mini-variant="false"
        mobile-breakpoint="720"
      >
        <v-list expand dense subheader>
          <v-subheader>
            舰船选择
          </v-subheader>
          <v-list-group
            v-for="classes in ships"
            :key="classes.label"
            v-model="classes.active"
            no-action
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title v-text="classes.label" class="body-2"></v-list-item-title>
              </v-list-item-content>
            </template>

            <template
              v-for="ship in classes.ships"
            >
              <template v-if="ship.children">
                <v-list-group
                  :key="ship.id"
                  sub-group
                  no-action
                >
                  <template v-slot:activator>
                    <v-list-item-content>
                      <v-list-item-title v-text="ship.prototype_name"></v-list-item-title>
                    </v-list-item-content>
                  </template>

                  <v-list-item
                    v-for="child in ship.children"
                    :key="child.id"
                    dense
                    link
                    class="pl-16"
                    @click="selectShip(child)"
                  >
                      <v-list-item-action class="mr-4">
                        <v-checkbox :input-value="activeShip && child.id == activeShip.id"></v-checkbox>
                      </v-list-item-action>
                      <v-list-item-content>
                      <v-list-item-title>
                        {{ child.subtype }}
                      </v-list-item-title>
                    </v-list-item-content>     
                  </v-list-item>
                </v-list-group>
              </template>
              <template v-else>
                <v-list-item
                  :key="ship.id"
                  dense
                  link
                  class="pl-8"
                  @click="selectShip(ship)"
                >
                  <v-list-item-action class="mr-4">
                      <v-checkbox :input-value="activeShip && ship.id == activeShip.id"></v-checkbox>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title v-text="ship.prototype_name"></v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
              </template>
            </template>
          </v-list-group>
        </v-list>
      </v-navigation-drawer>
    </v-card>
    <v-card v-if="activeShip">
      <v-card-title>
        [{{ activeShip.class }}] {{ activeShip.prototype_name }}{{ activeShip.subtype ? ' - '+activeShip.subtype : '' }}
      </v-card-title>
      <v-subheader>
        所属：{{ activeShip.company }}
      </v-subheader>
      <v-subheader>
        战略性能：{{ formatFeature(activeShip.strategy) }}
      </v-subheader>
      <v-subheader>
        战术性能：{{ formatFeature(activeShip.tactic) }}
      </v-subheader>
    </v-card>
    <v-card v-for="collection in research_tree" :key="activeShip.id + '-count-'+collection.count" flat class="mt-2">
      <v-card-title>
        研发{{ collection.count }}次
      </v-card-title>
      <v-expansion-panels accordion>
        <v-expansion-panel v-for="(item, idx) in collection.collection" :key="idx">
          <v-expansion-panel-header class="success--text">
            <template #default>
              {{ item.filter.join(' + ') }} ({{ item.data.length }})
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-list>
              <v-list-item v-for="ship in item.data" :key="'ship-'+ship.id" dense class="body-2 pl-0">
                <v-list-item-content class="py-0">
                  <v-row no-gutters>
                    <v-col cols="2" :class="activeShip.id == ship.id ? 'font-weight-bold primary--text' : ''">
                      [{{ ship.class }}]
                    </v-col>
                    <v-col :class="activeShip.id == ship.id ? 'font-weight-bold primary--text' : ''">
                      {{ ship.prototype_name }}{{ ship.subtype ? ' - ' + ship.subtype : '' }}
                    </v-col>
                  </v-row>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script>
import {
  defineComponent,
  ref,
  watch,
  inject
} from '@vue/composition-api';
import data from '@/data/data.json';
import _ from 'lodash';

export default defineComponent({
  setup(){
    const ships = ref([]);
    const menu = inject('menu');
    data.forEach(d => {
      const _class = d.class;
      const idx = ships.value.findIndex( x => x?.label == _class );
      const item = JSON.parse(JSON.stringify(d));

      const _proto = idx != -1 ? ships.value[idx].ships.find( x => x.prototype_name == d.prototype_name ) : null; 
      
      if( idx == -1 ){
        if( d?.subtype ){        
          item.children = [JSON.parse(JSON.stringify(d))];
        }
        ships.value.push({
          label: _class,
          active: false,
          ships: [item]
        });
      }else{
        // 原型已经存在
        if( _proto ){
          if( !_proto.children ){
            _proto.children = [];
          }
          _proto.children.push(JSON.parse(JSON.stringify(d)));
        }else{
          if( d?.subtype ){        
            item.children = [JSON.parse(JSON.stringify(d))];            
          }
          ships.value[idx].ships.push(item)
        }
      }
    });

    const activeShip = ref(null);

    const findMatches = (id, company, strategy, tactic ) => {
      const find = data.filter( x => {
        return x.id == id || 
        (
          ( !company || x.company == company ) 
          && ( !strategy || x.strategy.indexOf(strategy) != -1 )
          && ( !tactic || x.tactic.indexOf(tactic) != -1)
        );
      });
      if( find?.length ){
        return {
          filter: _.without([company, strategy, tactic], undefined, null),
          data: find.map( x => _.pick(x, ['id', 'class', 'prototype_name', 'subtype']) )
        }
      }else{
        return null;
      }
    };

    const research_tree = ref([]);
    watch( () => activeShip.value, v => {
      if( v ){        
        // 2次匹配：company/战略性能/战术性能 3选2
        let matches_2 = [];
        // company + 战略
        if( v.strategy?.length ){
          v.strategy.forEach( s => {
            const find = findMatches(v.id, v.company, s, null);
            if( find ){
              matches_2.push(find);
            }
          });
        }
        // company + 战术
        if( v.tactic?.length ){
          v.tactic.forEach( t => {
            const find = findMatches(v.id, v.company, null, t);
            if( find ){
              matches_2.push(find);
            }
          });
        }
        // 战略 + 战术
        if( v.strategy?.length && v.tactic?.length ){
          v.strategy.forEach( s => {
            v.tactic.forEach( t => {
              const find = findMatches(v.id, null, s, t);
              if( find ){
                matches_2.push(find);
              }
            });
          });
        }

        // 3次匹配：company + 战略性能 + 战术性能
        let matches_3 = [];
        if( v.strategy?.length && v.tactic?.length ){          
          v.strategy.forEach( s => {
            v.tactic.forEach( t => {
              const find = findMatches(v.id, v.company, s, t);
              if( find ){
                matches_3.push(find);
              }
            });
          });
        }
        research_tree.value = [];
        if( matches_2?.length ){
          research_tree.value.push({
            count: 2,
            collection: matches_2
          });
        }
        if( matches_3?.length ){
          research_tree.value.push({
            count: 3,
            collection: matches_3
          });
        }
      }else{
        research_tree.value = [];
      }
    })

    return {
      menu,
      data,
      ships,
      activeShip,
      research_tree
    }
  },
  data(){
    return {

    }
  },
  methods: {
    selectShip(item) {
      this.activeShip = this.activeShip?.id == item.id ? null : item;
    },
    formatFeature(array) {
      return array?.length ? array.join(', ') : '无';
    },
    formatMatchers(array) {
      const result = array.map( x => '[' + x.class + '] ' + x.prototype_name + ( x?.subtype ? ' - ' + x.subtype : '') );
      return result.join(', ');
    }
  }
})
</script>
